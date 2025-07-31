from ninja import NinjaAPI, Schema
from typing import List, Optional
from .models import Member, Region
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection

api = NinjaAPI(title="Tenant API", urls_namespace="tenant_api")

class RegionSchema(Schema):
    id: int
    name: str    
class MemberUpdateSchema(Schema):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    region: str

class MemberResponseSchema(Schema):
    id: int
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime
    region: RegionSchema
class ErrorSchema(Schema):
    detail: str

@api.exception_handler(ObjectDoesNotExist)
def object_does_not_exist_handler(request, exc):
    return api.create_response(
        request,
        {"detail": "Object not found."},
        status=404
    )

# debug statement to check active schema
@api.get("/ping")
def ping(request):
    from django.db import connection
    print("👀 Active schema:", connection.schema_name)
    return {"message": "pong"}

@api.get("/region/{region_id}/members", response=List[MemberResponseSchema])
def list_members(request, region_id: int):
    print("👀 Active schema (view-level):", connection.schema_name)

    region = get_object_or_404(Region, id=region_id)
    return region.members.all()

@api.post("/region/{region_id}/members", response=MemberResponseSchema)
def create_member(request, region_id: int, payload: MemberUpdateSchema):
    region = get_object_or_404(Region, id=region_id)
    member = Member.objects.create(
        name=payload.name,
        phone=payload.phone,
        email=payload.email,
        region=region
    )
    return member

@api.get("/region/{region_id}/members/{member_id}", response=MemberResponseSchema)
def get_member(request, region_id: int, member_id: int):
    member = get_object_or_404(Member, id=member_id, region_id=region_id)
    return member

@api.put("/region/{region_id}/members/{member_id}", response=MemberResponseSchema)
def update_member(request, region_id: int, member_id: int, payload: MemberUpdateSchema):
    member = get_object_or_404(Member, id=member_id, region_id=region_id)
    member.name = payload.name
    member.phone = payload.phone
    member.email = payload.email
    member.save()
    return member

@api.delete("/region/{region_id}/members/{member_id}", response={200: None})
def delete_member(request, region_id: int, member_id: int):
    member = get_object_or_404(Member, id=member_id, region_id=region_id)
    member.delete()
    return 200
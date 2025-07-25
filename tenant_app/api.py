from ninja import NinjaAPI, Schema, Router
from typing import List, Optional
from .models import Member, Region
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection

from django.db import connection
print("👀 Current schema:", connection.schema_name)

router = Router(tags=["Tenant"])
class RegionSchema(Schema):
    id: int
    name: str    
class MemberUpdateSchema(Schema):
    name: str
    region_id: str
    phone: Optional[str] = None
    email: Optional[str] = None    
class MemberResponseSchema(Schema):
    id: int
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime
    region: RegionSchema

class ErrorSchema(Schema):
    detail: str

@router.get("/region/{region_id}/members", response=List[MemberResponseSchema])
def list_members(request, region_id: int):
    # The current tenant schema is already set by django-tenants middleware
    print("👀 Active schema:", request.tenant.schema_name)  # DEBUG line
    region = get_object_or_404(Region, id=region_id)
    return region.members.all()

@router.post("/region/{region_id}/members", response=MemberResponseSchema)
def create_member(request, region_id: int, payload: MemberUpdateSchema):
    # The current tenant schema is already set by django-tenants middleware
    region = get_object_or_404(Region, id=region_id)
    member = Member.objects.create(
        name=payload.name,
        phone=payload.phone,
        email=payload.email,
        region=region
    )
    return member

@router.get("/region/{region_id}/members/{member_id}", response=MemberResponseSchema)
def get_member(request, region_id: int, member_id: int):
    get_object_or_404(Region, id=region_id)
    member = get_object_or_404(Member, id=member_id, region_id=region_id)
    return member

@router.put("/region/{region_id}/members/{member_id}", response=MemberResponseSchema)
def update_member(request, region_id: int, member_id: int, payload: MemberUpdateSchema):
    member = get_object_or_404(Member, id=member_id, region_id=region_id)
    member.name = payload.name
    if payload.phone is not None:
        member.phone = payload.phone
    if payload.email is not None:
        member.email = payload.email
    member.save()
    return member

@router.delete("/region/{region_id}/members/{member_id}", response={200: None})
def delete_member(request, region_id: int, member_id: int):
    member = get_object_or_404(Member, id=member_id, region_id=region_id)
    member.delete()
    return 200
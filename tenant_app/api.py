from ninja import NinjaAPI, Schema
from typing import List, Optional
from .models import Member
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection

api = NinjaAPI(title="Tenant API", urls_namespace="tenant_api")
    
class MemberUpdateSchema(Schema):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None

class MemberResponseSchema(Schema):
    id: int
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime

class ErrorSchema(Schema):
    detail: str

@api.exception_handler(ObjectDoesNotExist)
def object_does_not_exist_handler(request, exc):
    return api.create_response(
        request,
        {"detail": "Object not found."},
        status=404
    )

@api.get("/members", response=List[MemberResponseSchema])
def list_members(request):
    # The current tenant schema is already set by django-tenants middleware
    return Member.objects.all()

@api.post("/members", response=MemberResponseSchema)
def create_member(request, payload: MemberUpdateSchema):
    # The current tenant schema is already set by django-tenants middleware
    member = Member.objects.create(
        name=payload.name,
        phone=payload.phone,
        email=payload.email
    )
    return member

@api.get("/members/{member_id}", response=MemberResponseSchema)
def get_member(request, member_id: int):
    member = Member.objects.get(id=member_id)
    return member

@api.put("/members/{member_id}", response=MemberResponseSchema)
def update_member(request, member_id: int, payload: MemberUpdateSchema):
    member = Member.objects.get(id=member_id)
    member.name = payload.name
    if payload.phone is not None:
        member.phone = payload.phone
    if payload.email is not None:
        member.email = payload.email
    member.save()
    return member

@api.delete("/members/{member_id}", response={200: None})
def delete_member(request, member_id: int):
    member = Member.objects.get(id=member_id)
    member.delete()
    return 200
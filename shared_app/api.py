from django.core.exceptions import ObjectDoesNotExist
from ninja import NinjaAPI, Schema
from typing import List
from .models import Client, Domain
from tenant_app.api import router as tenant_router  # Import the router

api = NinjaAPI(title="Shared API", urls_namespace="shared_api")

@api.exception_handler(ObjectDoesNotExist)
def object_does_not_exist_handler(request, exc):
    return api.create_response(
        request,
        {"detail": "Object not found."},
        status=404
    )

class ClientSchema(Schema):
    id: int
    name: str
    schema_name: str

class DomainSchema(Schema):
    id: int
    domain: str
    tenant_id: int

@api.get("/clients", response=List[ClientSchema])
def list_clients(request):
    return Client.objects.all()

@api.get("/domains", response=List[DomainSchema])
def list_domains(request):
    return Domain.objects.all()

# Add the tenant_app router
api.add_router("/", tenant_router)
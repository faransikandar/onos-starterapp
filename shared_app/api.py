from ninja import NinjaAPI, Schema
from typing import List
from .models import Client, Domain
from django.db import connection

api = NinjaAPI(title="Shared API", urls_namespace="shared_api")

class ClientSchema(Schema):
    id: int
    name: str
    schema_name: str

class DomainSchema(Schema):
    id: int
    domain: str
    tenant_id: int

# debug statement to check active schema
@api.get("/ping")
def ping(request):
    from django.db import connection
    print("👀 Active schema:", connection.schema_name)
    return {"message": "pong"}

@api.get("/clients", response=List[ClientSchema])
def list_clients(request):
    return Client.objects.all()

@api.get("/domains", response=List[DomainSchema])
def list_domains(request):
    return Domain.objects.all()
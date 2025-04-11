from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.tenant import TenantBase
from config.database import engine, Base, get_db, SessionLocal
from typing import List
from controllers.tenant import (
    create_tenant, get_tenant, update_tenant, 
    delete_tenant, get_all_tenants, get_tenant_by_name
)
from schemas.tenant import TenantResponse, TenantCreate, TenantUpdate
from models.user import User
from controllers.auth import get_current_user
from utils.authorization import is_superuser_required
from config.parameters import *

# ---- Routes ----
tenant_router = APIRouter(tags=["Tenants"])
Base.metadata.create_all(bind=engine)

@tenant_router.on_event('startup')
async def populate_super_tenant():
    tenant = {
        "name": USER_NAME,
        "slug": SLUG,
        "email": EMAIL,
        "subscription_plan": SUBSCRIPTION_PLAN,
        "subscription_status": SUBSCRIPTION_STATUS
    }

    admin_tenant = TenantBase(**tenant)
    db = SessionLocal()
    try:
        db_tenant = get_tenant_by_name(db, tenant_slug_name=admin_tenant.slug)
    except:  
        db_tenant = None 

    if not db_tenant:
        print("Super Tenant setup")
        create_tenant(db=db, tenant_data=admin_tenant)

    db.close()

@tenant_router.post("/create_tenant/", response_model=TenantResponse)
def create(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_superuser_required)
):
    return create_tenant(db, tenant_data)

@tenant_router.get("/get_single_tanent/{tenant_id}", response_model=TenantResponse)
def read(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_superuser_required)
):
    return get_tenant(db, tenant_id)

@tenant_router.get("/get_tenanent_by_slug/{tenant_slug_name}", response_model=TenantResponse)
def read_tenant_by_name(
    tenant_slug_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_superuser_required)
):
    return get_tenant_by_name(db, tenant_slug_name)

@tenant_router.get("/get_all_tanent", response_model=List[TenantResponse])
def read_tenants(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_superuser_required)
):
    return get_all_tenants(db, skip, limit)

@tenant_router.put("/update_tenant/{tenant_id}", response_model=TenantResponse)
def update(
    tenant_id: int,
    update_data: TenantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_superuser_required)
):
    return update_tenant(db, tenant_id, update_data)

@tenant_router.delete("/delete_tenant/{tenant_id}")
def delete(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_superuser_required)
):
    return delete_tenant(db, tenant_id)

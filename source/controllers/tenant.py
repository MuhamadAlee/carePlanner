from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4
from config.parameters import *
from models.tenant import Tenant
from schemas.tenant import TenantCreate, TenantUpdate
from sqlalchemy import text
from config.database import create_tenant_schema_and_tables


def get_tenant(db: Session, tenant_id: int):
    """Retrieve a tenant by its unique identifier.
    
    Args:
        db (Session): Database session.
        tenant_id (int): Unique identifier of the tenant.
    
    Returns:
        Tenant: The retrieved tenant object if found.
    
    Raises:
        HTTPException: If the tenant is not found.
    """
    try: 
        tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")
        return tenant
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_all_tenants(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all tenants with optional pagination.
    
    Args:
        db (Session): Database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
    
    Returns:
        List[Tenant]: List of tenants.
    """
    try: 
        return db.query(Tenant).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_tenant_by_name(db: Session, tenant_slug_name: str):
    """Retrieve a tenant by its unique slug name.
    
    Args:
        db (Session): Database session.
        tenant_slug_name (str): Slug name of the tenant.
    
    Returns:
        Tenant: The retrieved tenant object if found.
    
    Raises:
        HTTPException: If the tenant is not found.
    """
    try:
        tenant = db.query(Tenant).filter(Tenant.slug == tenant_slug_name).first()
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")
        return tenant
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_tenant(db: Session, tenant_data: TenantCreate):
    """Create a new tenant in the database.
    
    Args:
        db (Session): Database session.
        tenant_data (TenantCreate): Tenant creation data.
    
    Returns:
        Tenant: The newly created tenant object.
    """
    try: 
        tenant = Tenant(**tenant_data.dict())
        db.add(tenant)
        db.flush()
        tenant_info = db.execute(text("SHOW search_path")).fetchall()[0][0]
        tenant_info = tenant_info.split(',')[-1].strip()
        db.commit()
        db.execute(text(f"SET search_path TO {tenant_info}"))
        db.refresh(tenant)
        if tenant.slug != SLUG:
            create_tenant_schema_and_tables(tenant.slug)
        return tenant
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def update_tenant(db: Session, tenant_id: int, update_data: TenantUpdate):
    """Update an existing tenant's details.
    
    Args:
        db (Session): Database session.
        tenant_id (int): Unique identifier of the tenant to be updated.
        update_data (TenantUpdate): Data containing the fields to update (partial updates allowed).
    
    Returns:
        Tenant: The updated tenant object.
    
    Raises:
        HTTPException: If the tenant is not found or update fails.
    """
    try: 
        tenant = get_tenant(db, tenant_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(tenant, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(tenant)
        return tenant
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def delete_tenant(db: Session, tenant_id: int):
    """Delete a tenant from the database.
    
    Args:
        db (Session): Database session.
        tenant_id (int): Unique identifier of the tenant to be deleted.
    
    Returns:
        dict: Message confirming tenant deletion.
    
    Raises:
        HTTPException: If the tenant is not found or deletion fails.
    """
    try: 
        tenant = get_tenant(db, tenant_id)
        db.delete(tenant)
        db.commit()
        return {"message": "Tenant deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

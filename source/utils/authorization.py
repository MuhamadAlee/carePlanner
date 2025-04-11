from functools import wraps
import asyncio
from controllers.auth import get_current_user
from models.user import User
from utils.auth_util import get_tenant_from_token
from fastapi import Depends, HTTPException
from controllers.role import get_role
from utils.tenant_util import is_tenant_active
from config.parameters import *
from config.database import get_db, get_db_tenant
from sqlalchemy.orm import Session


async def is_superuser_required(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant: str = Depends(get_tenant_from_token)
):
    # Check tenant status (uncomment this line if tenant validation is needed)
    if not is_tenant_active(tenant):
        raise HTTPException(status_code=403, detail="Tenant is blocked")
    
    # Check if the user has superuser role
    current_user_role = get_role(db, current_user.role_id).role_name
    if current_user_role != SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="Superuser access required")

    # Check if the user is active
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="User is blocked")

    return current_user



async def is_admin_required(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant: str = Depends(get_tenant_from_token)  # optional, include if you need it
):
    # Optional: tenant check
    if not is_tenant_active(tenant):
        raise HTTPException(status_code=403, detail="Tenant is blocked")

    current_user_role = get_role(db, current_user.role_id).role_name

    if current_user_role not in [ADMIN, SUPER_ADMIN]:
        raise HTTPException(status_code=403, detail="Admin access required")
    elif not current_user.is_active:
        raise HTTPException(status_code=403, detail="User is blocked")

    return current_user 

async def is_office_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant: str = Depends(get_tenant_from_token)
):
    # Check tenant status (uncomment this line if tenant validation is needed)
    if not is_tenant_active(tenant):
        raise HTTPException(status_code=403, detail="Tenant is blocked")
    
    # Check if the user has one of the allowed roles
    current_user_role = get_role(db, current_user.role_id).role_name
    if current_user_role not in [ADMIN, SUPER_ADMIN, OFFICE_USER]:
        raise HTTPException(status_code=403, detail="Access Denied")

    # Check if the user is active
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="User is blocked")

    return current_user 

async def is_care_coordinator_required(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant: str = Depends(get_tenant_from_token)
):
    # Check tenant status (uncomment this line if tenant validation is needed)
    if not is_tenant_active(tenant):
        raise HTTPException(status_code=403, detail="Tenant is blocked")
    
    # Check if the user has one of the allowed roles
    current_user_role = get_role(db, current_user.role_id).role_name
    if current_user_role not in [ADMIN, SUPER_ADMIN, OFFICE_USER, CARE_COORDINATOR]:
        raise HTTPException(status_code=403, detail="Access Denied")

    # Check if the user is active
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="User is blocked")

    return current_user 

async def is_supervisor(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant: str = Depends(get_tenant_from_token)
):
    # Check tenant status (uncomment this line if tenant validation is needed)
    if not is_tenant_active(tenant):
        raise HTTPException(status_code=403, detail="Tenant is blocked")
    
    # Check if the user has one of the allowed roles
    current_user_role = get_role(db, current_user.role_id).role_name
    if current_user_role not in [ADMIN, SUPER_ADMIN, OFFICE_USER, CARE_COORDINATOR, SUPERVISOR]:
        raise HTTPException(status_code=403, detail="Access Denied")

    # Check if the user is active
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="User is blocked")

    return current_user 


async def is_carer_required(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant: str = Depends(get_tenant_from_token)
):
    # Check tenant status (uncomment this line if tenant validation is needed)
    if not is_tenant_active(tenant):
        raise HTTPException(status_code=403, detail="Tenant is blocked")
    
    # Check if the user has one of the allowed roles
    current_user_role = get_role(db, current_user.role_id).role_name
    if current_user_role not in [ADMIN, SUPER_ADMIN, OFFICE_USER, CARE_COORDINATOR, SUPERVISOR, CARER]:
        raise HTTPException(status_code=403, detail="Access Denied")

    # Check if the user is active
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="User is blocked")

    return current_user 

async def is_yourself(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant: str = Depends(get_tenant_from_token)
):
    # Check tenant status (uncomment this line if tenant validation is needed)
    if not is_tenant_active(tenant):
        raise HTTPException(status_code=403, detail="Tenant is blocked")
    
    # Check if the user role is valid
    current_user_role = get_role(db, current_user.role_id).role_name
    if current_user_role not in ROLES:  # Assuming ROLES is defined as a list of allowed roles
        raise HTTPException(status_code=403, detail="Access denied")

    # Check if the user is active
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="User is blocked")

    return current_user 

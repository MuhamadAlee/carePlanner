from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from config.database import get_db, get_db_by_tenant
from typing import List
from controllers.role import create_role, get_role, update_role, delete_role,\
    get_all_roles, get_role_by_name, first_time_bulk_role_creation
from utils.tenant_util import get_super_tenant_id
from schemas.role import RoleResponse, RoleCreate, RoleUpdate
from config.database import engine, Base, get_db, SessionLocal
from schemas.role import RoleBase
from controllers.auth import get_current_user
from models.user import User
from config.parameters import *
from utils.authorization import is_care_coordinator_required, is_superuser_required

role_router = APIRouter(tags=["Roles"])
Base.metadata.create_all(bind=engine)

@role_router.on_event('startup')
async def populate_super_role():
    role = {
        "role_name": ROLE_NAME,
        "description": ROLE_DESCRIPTION
        }
    db= SessionLocal()
    super_admin_role = RoleCreate(**role)
    
    try:
        db_role = get_role_by_name(db, role_name=super_admin_role.role_name)
    except:  
        db_role = None 

    if not db_role:
        print("Super Role setup")
        first_time_bulk_role_creation(db, "super_tenant")

    db.close()

# @role_router.post("/create_role/", response_model=RoleResponse, dependencies=[Depends(get_current_user)])
# def create(role_data: RoleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_care_coordinator_required)):
#     return create_role(db, role_data)

# @role_router.post("/create_role/{tenant_slug}/", response_model=RoleResponse, dependencies=[Depends(get_current_user)])
# def create_role_by_tenant( tenant_slug: str, role_data: RoleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_superuser_required)):
#     db = get_db_by_tenant(tenant_slug)
#     return create_role(next(db), role_data)

# @role_router.get("/get_role/{role_id}", response_model=RoleResponse, dependencies=[Depends(get_current_user)])
# def read(role_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_care_coordinator_required)):
#     return get_role(db, role_id)


@role_router.get("/get_all_roles_by_tenant/{tenant_slug}/", response_model=List[RoleResponse], dependencies=[Depends(get_current_user)])
def read_by_tenant(tenant_slug:str, skip: int = 0, limit: int = 10,  db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_superuser_required)):
    db = get_db_by_tenant(tenant_slug)
    return get_all_roles(next(db), skip, limit)

@role_router.get("/get_all_roles/", response_model=List[RoleResponse], dependencies=[Depends(get_current_user)])
def read_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_care_coordinator_required)):
    return get_all_roles(db, skip, limit)

# @role_router.put("/update_role/{role_id}", response_model=RoleResponse, dependencies=[Depends(get_current_user)])
# def update(role_id: int, update_data: RoleUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _=Depends(is_care_coordinator_required)):
#     return update_role(db, role_id, update_data)

# @role_router.put("/update_role_by_tenant/{role_id}/{tenant_slug}", response_model=RoleResponse, dependencies=[Depends(get_current_user)])
# def update_tenant(tenant_slug: str, role_id: int, update_data: RoleUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_superuser_required)):
#     db = get_db_by_tenant(tenant_slug)
#     return update_role(next(db), role_id, update_data)

# @role_router.delete("/delete_role/{role_id}", dependencies=[Depends(get_current_user)])
# def delete(role_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _=Depends(is_care_coordinator_required)):
#     return delete_role(db, role_id)

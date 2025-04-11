from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserBase, UserCreate, UserUpdate, UserResponse
from config.database import engine, Base, get_db, SessionLocal, get_db_by_tenant
from utils.role_util import get_super_role_id
from utils.util import hash_password
from typing import List
from controllers.user import (
    create_user, get_user, update_user, 
    delete_user, get_all_users, get_user_by_email
)
from controllers.auth import get_current_user
from utils.authorization import is_care_coordinator_required, is_yourself,\
     is_admin_required, is_superuser_required, is_office_user
from utils.role_util import get_role
from models.user import User
from config.parameters import *

# ---- Routes ----
user_router = APIRouter(tags=["Users"])
Base.metadata.create_all(bind=engine)

@user_router.on_event('startup')
async def populate_super_user():
    role_id = get_super_role_id()
    user = {
        "name": SUPER_USER_NAME,
        "email": SUPER_USER_EMAIL,
        "password": hash_password(SUPER_USER_PASSWORD),
        "role_id": role_id,
        "contact": SUPER_USER_CONTACT,
        "address": SUPER_USER_ADDRESS,
        "employee_type": SUPER_USER_EMPLOYEE_TYPE,
        "working_hours": SUPER_USER_HOURS,
        "working_hour_rate": 0,
        "travel_rate": 0,
        "is_active": True,
        "dbs_status": True
    }

    admin_user = UserCreate(**user)
    db= SessionLocal()
    try:
        db_user = get_user_by_email(db, email=admin_user.email)
    except:
        db_user = None 

    if not db_user:
        print("Super User setup")
        create_user(db=db, user_data=admin_user)

    db.close()

@user_router.post("/create_user/", response_model=UserResponse, dependencies=[Depends(get_current_user)])

def create(user_data: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _=Depends(is_office_user)):
    user_data.password = hash_password(user_data.password)
    return create_user(db, user_data)

@user_router.post("/create_user_by_tenant/{tenant_slug}/", response_model=UserResponse, dependencies=[Depends(get_current_user)])
def create_user_by_tenant(tenant_slug:str, user_data: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _=Depends(is_superuser_required)):
    user_data.password = hash_password(user_data.password)
    db = get_db_by_tenant(tenant_slug)
    return create_user(next(db), user_data)

@user_router.get("/get_single_user/{user_id}", response_model=UserResponse, dependencies=[Depends(get_current_user)])

def read(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _=Depends(is_care_coordinator_required)):
    return get_user(db, user_id)

@user_router.get("/get_yourself/", response_model=UserResponse, dependencies=[Depends(get_current_user)])
def read_yourself(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _=Depends(is_yourself)):
    return get_user(db, current_user.user_id)

@user_router.get("/get_user_by_email/{email}", response_model=UserResponse, dependencies=[Depends(get_current_user)])
def read_user_by_email(email: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _=Depends(is_care_coordinator_required)):
    return get_user_by_email(db, email)

@user_router.get("/get_all_users/", response_model=List[UserResponse], dependencies=[Depends(get_current_user)])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _= Depends(is_admin_required)):
    return get_all_users(db, skip, limit)

@user_router.get("/get_all_users_by_tenant/{tenant_slug}/", response_model=List[UserResponse], dependencies=[Depends(get_current_user)])
def read_users_by_tenant(tenant_slug:str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _=Depends(is_superuser_required)):
    db = get_db_by_tenant(tenant_slug)
    return get_all_users(next(db), skip, limit)

@user_router.put("/update_user/{user_id}", response_model=UserResponse, dependencies=[Depends(get_current_user)])
def update(user_id: int, update_data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _=Depends(is_office_user)):
    update_data.password = hash_password(update_data.password)
    current_user_role = get_role(db, current_user.role_id).role_name
    return update_user(db, current_user_role, user_id, update_data)

@user_router.put("/update_user_by_tenant/{user_id}/{tenant_slug}/", response_model=UserResponse, dependencies=[Depends(get_current_user)])
def update_user_by_tenant_id(tenant_slug: str, user_id: int, update_data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _=Depends(is_superuser_required)):
    update_data.password = hash_password(update_data.password)
    db = get_db_by_tenant(tenant_slug)
    return update_user(next(db), SUPER_ADMIN, user_id, update_data)

# @user_router.put("/update_yourself/", response_model=UserResponse, dependencies=[Depends(get_current_user)])
# def update_yourself(update_data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _=Depends(is_office_user)):
#     update_data.password = hash_password(update_data.password)
#     return update_user(db, current_user.user_id, update_data)

@user_router.delete("/delete_user/{user_id}", dependencies=[Depends(get_current_user)])
def delete(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _=Depends(is_office_user)):
    return delete_user(db, user_id)

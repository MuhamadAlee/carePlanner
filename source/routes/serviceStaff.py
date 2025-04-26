from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.serviceStaff import ServiceStaffCreate, ServiceStaffUpdate, ServiceStaffResponse
from config.database import get_db, engine, Base
from controllers.serviceStaff import (
    create_service_staff, get_service_staff, update_service_staff, 
    delete_service_staff, get_all_service_staff, get_service_staff_by_service_id,
    get_service_staff_by_user_id
)
from controllers.auth import get_current_user
from utils.authorization import is_supervisor
from models.serviceStaff import ServiceStaff
from models.user import User
from typing import List

# ---- Routes ----
service_staff_router = APIRouter(tags=["Service Staff"])
Base.metadata.create_all(bind=engine)

@service_staff_router.post("/create_service_staff/", response_model=ServiceStaffResponse)
def create(
    service_staff_data: ServiceStaffCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return create_service_staff(db, service_staff_data)

@service_staff_router.get("/get_single_service_staff/{service_staff_id}", response_model=ServiceStaffResponse)
def read(
    service_staff_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_service_staff(db, service_staff_id)

@service_staff_router.get("/get_single_service_by_service_id/{service_id}", response_model=List[ServiceStaffResponse])
def read_by_service_id(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_service_staff_by_service_id(db, service_id)

@service_staff_router.get("/get_single_service_by_user_id/{user_id}", response_model=List[ServiceStaffResponse])
def read_by_user_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_service_staff_by_user_id(db, user_id)

@service_staff_router.get("/get_all_service_staff/", response_model=List[ServiceStaffResponse])
def read_service_staff(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_all_service_staff(db, skip, limit)

@service_staff_router.put("/update_service_staff/{service_staff_id}", response_model=ServiceStaffResponse)
def update(
    service_staff_id: int,
    update_data: ServiceStaffUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return update_service_staff(db, service_staff_id, update_data)

@service_staff_router.delete("/delete_service_staff/{service_staff_id}")
def delete(
    service_staff_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return delete_service_staff(db, service_staff_id)

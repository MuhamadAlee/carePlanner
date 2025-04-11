from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.rotaStaff import RotaStaffCreate, RotaStaffUpdate, RotaStaffResponse
from config.database import get_db, engine, Base
from controllers.rotaStaff import (
    create_rota_staff, get_rota_staff, update_rota_staff, 
    delete_rota_staff, get_all_rota_staff, get_rota_staff_by_rota_id,
    get_rota_staff_by_user_id
)
from controllers.auth import get_current_user
from utils.authorization import is_supervisor
from models.rotaStaff import RotaStaff
from models.user import User
from typing import List

# ---- Routes ----
rota_staff_router = APIRouter(tags=["Rota Staff"])
Base.metadata.create_all(bind=engine)

@rota_staff_router.post("/create_rota_staff/", response_model=RotaStaffResponse)
def create(
    rota_staff_data: RotaStaffCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return create_rota_staff(db, rota_staff_data)

@rota_staff_router.get("/get_single_rota_staff/{rota_staff_id}", response_model=RotaStaffResponse)
def read(
    rota_staff_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_rota_staff(db, rota_staff_id)

@rota_staff_router.get("/get_single_rota_by_rota_id/{rota_id}", response_model=List[RotaStaffResponse])
def read_by_rota_id(
    rota_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_rota_staff_by_rota_id(db, rota_id)

@rota_staff_router.get("/get_single_rota_by_user_id/{user_id}", response_model=List[RotaStaffResponse])
def read_by_user_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_rota_staff_by_user_id(db, user_id)

@rota_staff_router.get("/get_all_rota_staff/", response_model=List[RotaStaffResponse])
def read_rota_staff(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_all_rota_staff(db, skip, limit)

@rota_staff_router.put("/update_rota_staff/{rota_staff_id}", response_model=RotaStaffResponse)
def update(
    rota_staff_id: int,
    update_data: RotaStaffUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return update_rota_staff(db, rota_staff_id, update_data)

@rota_staff_router.delete("/delete_rota_staff/{rota_staff_id}")
def delete(
    rota_staff_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return delete_rota_staff(db, rota_staff_id)

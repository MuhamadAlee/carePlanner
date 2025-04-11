from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.rotaMedication import RotaMedicationCreate, RotaMedicationUpdate, RotaMedicationResponse
from config.database import get_db, engine, Base
from controllers.rotaMedication import (
    create_rota_medication, get_rota_medication, update_rota_medication,
    delete_rota_medication, get_all_rota_medications, get_rota_medication_by_rota_id
)
from controllers.auth import get_current_user
from utils.authorization import is_supervisor
from models.rotaMedication import RotaMedication
from models.user import User
from typing import List

# ---- Routes ----
rota_medication_router = APIRouter(tags=["Rota Medications"])
Base.metadata.create_all(bind=engine)

@rota_medication_router.post("/create_rota_medication/", response_model=RotaMedicationResponse)
def create(
    rota_medication_data: RotaMedicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return create_rota_medication(db, rota_medication_data)

@rota_medication_router.get("/get_single_rota_medication/{medication_id}", response_model=RotaMedicationResponse)
def read(
    medication_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_rota_medication(db, medication_id)

@rota_medication_router.get("/get_single_rota_medication_by_rota_id/{rota_id}", response_model=List[RotaMedicationResponse])
def read_by_rota_id(
    rota_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_rota_medication_by_rota_id(db, rota_id)

@rota_medication_router.get("/get_all_rota_medications/", response_model=List[RotaMedicationResponse])
def read_rota_medications(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_all_rota_medications(db, skip, limit)

@rota_medication_router.put("/update_rota_medication/{medication_id}", response_model=RotaMedicationResponse)
def update(
    medication_id: int,
    update_data: RotaMedicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return update_rota_medication(db, medication_id, update_data)

@rota_medication_router.delete("/delete_rota_medication/{medication_id}")
def delete(
    medication_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return delete_rota_medication(db, medication_id)

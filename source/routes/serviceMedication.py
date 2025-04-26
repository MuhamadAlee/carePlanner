from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.serviceMedication import ServiceMedicationCreate, ServiceMedicationUpdate, ServiceMedicationResponse
from config.database import get_db, engine, Base
from controllers.serviceMedication import (
    create_service_medication, get_service_medication, update_service_medication,
    delete_service_medication, get_all_service_medications, get_service_medication_by_service_id,
    get_service_medication_by_roster_id
)
from controllers.auth import get_current_user
from utils.authorization import is_supervisor, is_carer_required
from models.ServiceMedication import ServiceMedication
from models.user import User
from typing import List

# ---- Routes ----
service_medication_router = APIRouter(tags=["Service Medications"])
Base.metadata.create_all(bind=engine)

@service_medication_router.post("/create_service_medication/", response_model=ServiceMedicationResponse)
def create(
    service_medication_data: ServiceMedicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return create_service_medication(db, service_medication_data)

@service_medication_router.get("/get_single_service_medication/{medication_id}", response_model=ServiceMedicationResponse)
def read(
    medication_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_service_medication(db, medication_id)

@service_medication_router.get("/get_single_service_medication_by_service_id/{service_id}", response_model=List[ServiceMedicationResponse])
def read_by_service_id(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_carer_required)
):
    return get_service_medication_by_service_id(db, service_id)

@service_medication_router.get("/get_single_service_medication_by_roster_id/{roster_id}", response_model=List[ServiceMedicationResponse])
def read_by_service_id(
    roster_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_carer_required)
):
    return get_service_medication_by_roster_id(db, current_user.user_id, current_user.role_id, roster_id)

@service_medication_router.get("/get_all_service_medications/", response_model=List[ServiceMedicationResponse])
def read_service_medications(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_all_service_medications(db, skip, limit)

@service_medication_router.put("/update_service_medication/{medication_id}", response_model=ServiceMedicationResponse)
def update(
    medication_id: int,
    update_data: ServiceMedicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return update_service_medication(db, medication_id, update_data)

@service_medication_router.delete("/delete_service_medication/{medication_id}")
def delete(
    medication_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return delete_service_medication(db, medication_id)

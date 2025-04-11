from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.visitMedication import VisitMedicationCreate, VisitMedicationUpdate, VisitMedicationResponse
from config.database import get_db, engine, Base
from controllers.visitMedication import (
    create_visit_medication, get_visit_medication, update_visit_medication, 
    delete_visit_medication, get_all_visit_medications, 
    get_visit_medication_by_medication_id, get_visit_medication_by_visit_id,
    get_refused_medication
)
from controllers.auth import get_current_user
from utils.authorization import is_supervisor
from models.visitMedication import VisitMedication
from models.user import User
from typing import List

# ---- Routes ----
visit_medication_router = APIRouter(tags=["Visit Medications"])
Base.metadata.create_all(bind=engine)

@visit_medication_router.post("/create_visit_medication/", response_model=VisitMedicationResponse)
def create(
    visit_medication_data: VisitMedicationCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return create_visit_medication(db, visit_medication_data)

@visit_medication_router.get("/get_single_visit_medication/{visit_medication_id}", response_model=VisitMedicationResponse)
def read(
    visit_medication_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_visit_medication(db, visit_medication_id)

@visit_medication_router.get("/get_single_visit_medication_by_medication_id/{medication_id}", response_model=List[VisitMedicationResponse])
def read_by_medication_id(
    medication_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_visit_medication_by_medication_id(db, medication_id)

@visit_medication_router.get("/get_single_visit_medication_by_visit_id/{visit_id}", response_model=List[VisitMedicationResponse])
def read_by_visit_id(
    visit_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_visit_medication_by_visit_id(db, visit_id)

@visit_medication_router.get("/get_all_visit_medications/", response_model=List[VisitMedicationResponse])
def read_visit_medications(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_all_visit_medications(db, skip, limit)

@visit_medication_router.put("/update_visit_medication/{visit_medication_id}", response_model=VisitMedicationResponse)
def update(
    visit_medication_id: int, 
    update_data: VisitMedicationUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return update_visit_medication(db, visit_medication_id, update_data)

@visit_medication_router.delete("/delete_visit_medication/{visit_medication_id}")
def delete(
    visit_medication_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return delete_visit_medication(db, visit_medication_id)


@visit_medication_router.get("/get_refused_visit_medication/", response_model=VisitMedicationResponse)
def read( 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_refused_medication(db)

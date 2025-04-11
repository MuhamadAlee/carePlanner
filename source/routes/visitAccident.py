from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.visitAccident import VisitAccidentCreate, VisitAccidentUpdate, VisitAccidentResponse
from config.database import get_db, engine, Base
from controllers.visitAccident import (
    create_visit_accident, get_visit_accident, update_visit_accident, 
    delete_visit_accident, get_all_visit_accidents,
    get_visit_accident_by_visit_id
)
from controllers.auth import get_current_user
from utils.authorization import is_supervisor
from models.visitAccident import VisitAccident
from models.user import User
from typing import List

# ---- Routes ----
visit_accident_router = APIRouter(tags=["Visit Accident"])
Base.metadata.create_all(bind=engine)

@visit_accident_router.post("/create_visit_accident/", response_model=VisitAccidentResponse)
def create(
    visit_accident_data: VisitAccidentCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return create_visit_accident(db, visit_accident_data)

@visit_accident_router.get("/get_single_visit_accident/{visit_accident_id}", response_model=VisitAccidentResponse)
def read(
    visit_accident_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_visit_accident(db, visit_accident_id)

@visit_accident_router.get("/get_single_visit_accident_by_visit_id/{visit_id}", response_model=List[VisitAccidentResponse])
def read(
    visit_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_visit_accident_by_visit_id(db, visit_id)

@visit_accident_router.get("/get_all_visit_accidents/", response_model=List[VisitAccidentResponse])
def read_visit_accidents(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_all_visit_accidents(db, skip, limit)

@visit_accident_router.put("/update_visit_accident/{visit_accident_id}", response_model=VisitAccidentResponse)
def update(
    visit_accident_id: int, 
    update_data: VisitAccidentUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return update_visit_accident(db, visit_accident_id, update_data)

@visit_accident_router.delete("/delete_visit_accident/{visit_accident_id}")
def delete(
    visit_accident_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return delete_visit_accident(db, visit_accident_id)

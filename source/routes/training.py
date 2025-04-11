from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.training import TrainingCreate, TrainingUpdate, TrainingResponse
from config.database import engine, Base, get_db, SessionLocal
from typing import List
from controllers.training import (
    create_training, get_training, update_training, 
    delete_training, get_all_trainings, get_raining_by_user
)
from controllers.auth import get_current_user
from utils.authorization import is_care_coordinator_required, is_yourself
from models.user import User

# ---- Routes ----
training_router = APIRouter(tags=["Training"])
Base.metadata.create_all(bind=engine)

@training_router.post("/create_training/", response_model=TrainingResponse)
def create(
    training_data: TrainingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_care_coordinator_required)
):
    return create_training(db, training_data)

@training_router.get("/get_single_training/{training_id}", response_model=TrainingResponse)
def read(
    training_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_care_coordinator_required)
):
    return get_training(db, training_id)

@training_router.get("/get_your_training/", response_model=List[TrainingResponse])
def read_your_training(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_yourself)
):
    return get_raining_by_user(db, current_user.user_id)

@training_router.get("/get_training_by_user_id/{user_id}", response_model=List[TrainingResponse])
def read_user_training(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_care_coordinator_required)
):
    return get_raining_by_user(db, user_id)

@training_router.get("/get_all_trainings/", response_model=List[TrainingResponse])
def read_trainings(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_care_coordinator_required)
):
    return get_all_trainings(db, skip, limit)

@training_router.put("/update_training/{training_id}", response_model=TrainingResponse)
def update(
    training_id: int,
    update_data: TrainingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_care_coordinator_required)
):
    return update_training(db, training_id, update_data)

@training_router.delete("/delete_training/{training_id}")
def delete(
    training_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_care_coordinator_required)
):
    return delete_training(db, training_id)

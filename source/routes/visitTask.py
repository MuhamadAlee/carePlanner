from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.visitTask import VisitTaskCreate, VisitTaskUpdate, VisitTaskResponse
from config.database import get_db, engine, Base
from controllers.visitTask import (
    create_visit_task, get_visit_task, update_visit_task, 
    delete_visit_task, get_all_visit_tasks,
    get_visit_task_by_task_id, get_visit_task_by_visit_id
)
from controllers.auth import get_current_user
from utils.authorization import is_supervisor
from models.visitTask import VisitTask
from models.user import User
from typing import List

# ---- Routes ----
visit_task_router = APIRouter(tags=["Visit Tasks"])
Base.metadata.create_all(bind=engine)

@visit_task_router.post("/create_visit_task/", response_model=VisitTaskResponse)
def create(
    visit_task_data: VisitTaskCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return create_visit_task(db, visit_task_data)

@visit_task_router.get("/get_single_visit_task/{visit_task_id}", response_model=VisitTaskResponse)
def read(
    visit_task_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_visit_task(db, visit_task_id)

@visit_task_router.get("/get_visit_task_by_visit_id/{visit_id}", response_model=List[VisitTaskResponse])
def read_visit_task_by_visit_id(
    visit_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_visit_task_by_visit_id(db, visit_id)

@visit_task_router.get("/get_visit_task_by_task_id/{task_id}", response_model=List[VisitTaskResponse])
def read_visit_task_by_task_id(
    task_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_visit_task_by_task_id(db, task_id)

@visit_task_router.get("/get_all_visit_tasks/", response_model=List[VisitTaskResponse])
def read_visit_tasks(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_all_visit_tasks(db, skip, limit)

@visit_task_router.put("/update_visit_task/{visit_task_id}", response_model=VisitTaskResponse)
def update(
    visit_task_id: int, 
    update_data: VisitTaskUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return update_visit_task(db, visit_task_id, update_data)

@visit_task_router.delete("/delete_visit_task/{visit_task_id}")
def delete(
    visit_task_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return delete_visit_task(db, visit_task_id)

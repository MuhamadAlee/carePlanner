from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.serviceTask import ServiceTaskCreate, ServiceTaskUpdate, ServiceTaskResponse
from config.database import get_db, engine, Base
from controllers.serviceTask import (
    create_service_task, get_service_task, update_service_task,
    delete_service_task, get_all_service_tasks, get_service_task_by_service_id,
    get_service_task_by_roster_id
)
from controllers.auth import get_current_user
from utils.authorization import is_supervisor,is_carer_required
from models.serviceTask import ServiceTask
from models.user import User
from typing import List

# ---- Routes ----
service_task_router = APIRouter(tags=["Service Tasks"])
Base.metadata.create_all(bind=engine)

@service_task_router.post("/create_service_task/", response_model=ServiceTaskResponse)
def create(
    service_task_data: ServiceTaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(is_supervisor)
):
    return create_service_task(db, service_task_data)

@service_task_router.get("/get_single_service_task/{task_id}", response_model=ServiceTaskResponse)
def read(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(is_supervisor)
):
    return get_service_task(db, task_id)

@service_task_router.get("/get_single_service_task_by_service_id/{service_id}", response_model=List[ServiceTaskResponse])
def read_by_service_id(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(is_carer_required)
):
    return get_service_task_by_service_id(db, service_id)

@service_task_router.get("/get_single_service_task_by_roster_id/{roster_id}", response_model=List[ServiceTaskResponse])
def read_by_roster_id(
    roster_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(is_carer_required)
):
    return get_service_task_by_roster_id(db, current_user.user_id, current_user.role_id, roster_id)

@service_task_router.get("/get_all_service_tasks/", response_model=List[ServiceTaskResponse])
def read_service_tasks(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(is_supervisor)
):
    return get_all_service_tasks(db, skip, limit)

@service_task_router.put("/update_service_task/{task_id}", response_model=ServiceTaskResponse)
def update(
    task_id: int,
    update_data: ServiceTaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(is_supervisor)
):
    return update_service_task(db, task_id, update_data)

@service_task_router.delete("/delete_service_task/{task_id}")
def delete(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(is_supervisor)
):
    return delete_service_task(db, task_id)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.rotaTask import RotaTaskCreate, RotaTaskUpdate, RotaTaskResponse
from config.database import get_db, engine, Base
from controllers.rotaTask import (
    create_rota_task, get_rota_task, update_rota_task,
    delete_rota_task, get_all_rota_tasks, get_rota_task_by_rota_id
)
from controllers.auth import get_current_user
from utils.authorization import is_supervisor
from models.rotaTask import RotaTask
from models.user import User
from typing import List

# ---- Routes ----
rota_task_router = APIRouter(tags=["Rota Tasks"])
Base.metadata.create_all(bind=engine)

@rota_task_router.post("/create_rota_task/", response_model=RotaTaskResponse)
def create(
    rota_task_data: RotaTaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(is_supervisor)
):
    return create_rota_task(db, rota_task_data)

@rota_task_router.get("/get_single_rota_task/{task_id}", response_model=RotaTaskResponse)
def read(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(is_supervisor)
):
    return get_rota_task(db, task_id)

@rota_task_router.get("/get_single_rota_task_by_rota_id/{rota_id}", response_model=List[RotaTaskResponse])
def read_by_rota_id(
    rota_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(is_supervisor)
):
    return get_rota_task_by_rota_id(db, rota_id)

@rota_task_router.get("/get_all_rota_tasks/", response_model=List[RotaTaskResponse])
def read_rota_tasks(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(is_supervisor)
):
    return get_all_rota_tasks(db, skip, limit)

@rota_task_router.put("/update_rota_task/{task_id}", response_model=RotaTaskResponse)
def update(
    task_id: int,
    update_data: RotaTaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(is_supervisor)
):
    return update_rota_task(db, task_id, update_data)

@rota_task_router.delete("/delete_rota_task/{task_id}")
def delete(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(is_supervisor)
):
    return delete_rota_task(db, task_id)

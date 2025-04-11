from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.rota import RotaCreate, RotaUpdate, RotaResponse
from config.database import get_db, engine, Base
from controllers.rota import (
    create_rota, get_rota, update_rota, 
    delete_rota, get_all_rotas, get_rota_by_client_id,
    get_rota_by_day_of_week, get_rota_by_visit_type
)
from controllers.auth import get_current_user
from utils.authorization import is_supervisor
from models.rota import Rota
from models.user import User
from typing import List

# ---- Routes ----
rota_router = APIRouter(tags=["Rotas"])
Base.metadata.create_all(bind=engine)

@rota_router.post("/create_rota/", response_model=RotaResponse)
def create(
    rota_data: RotaCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return create_rota(db, rota_data)

@rota_router.get("/get_single_rota/{rota_id}", response_model=RotaResponse)
def read(
    rota_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_rota(db, rota_id)

@rota_router.get("/get_single_rota_by_client/{client_id}", response_model=List[RotaResponse])
def read_by_client(
    client_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_rota_by_client_id(db, client_id)

@rota_router.get("/get_rotas_by_day/{client_id}/{day_of_week}", response_model=List[RotaResponse])
def read_rotas_by_day(
    client_id: int, 
    day_of_week: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_rota_by_day_of_week(db, client_id, day_of_week)

@rota_router.get("/get_rotas_by_visit_type/{client_id}/{visit_type}", response_model=List[RotaResponse])
def read_rotas_by_visit_type(
    client_id: int, 
    visit_type: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_rota_by_visit_type(db, client_id, visit_type)

@rota_router.get("/get_all_rotas/", response_model=List[RotaResponse])
def read_rotas(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_all_rotas(db, skip, limit)

@rota_router.put("/update_rota/{rota_id}", response_model=RotaResponse)
def update(
    rota_id: int, 
    update_data: RotaUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return update_rota(db, rota_id, update_data)

@rota_router.delete("/delete_rota/{rota_id}")
def delete(
    rota_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return delete_rota(db, rota_id)

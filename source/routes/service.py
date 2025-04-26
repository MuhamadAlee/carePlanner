from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.service import ServiceCreate, ServiceUpdate, ServiceResponse
from config.database import get_db, engine, Base
from controllers.service import (
    create_service, get_service, update_service, 
    delete_service, get_all_services, get_service_by_client_id,
    get_service_by_day_of_week, get_service_by_visit_type
)
from controllers.auth import get_current_user
from utils.authorization import is_supervisor, is_carer_required
from models.service import Service
from models.user import User
from typing import List

# ---- Routes ----
service_router = APIRouter(tags=["Services"])
Base.metadata.create_all(bind=engine)

@service_router.post("/create_service/", response_model=ServiceResponse)
def create(
    service_data: ServiceCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return create_service(db, service_data)

@service_router.get("/get_single_service/{service_id}", response_model=ServiceResponse)
def read(
    service_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_service(db, service_id)

@service_router.get("/get_single_service_by_client/{client_id}", response_model=List[ServiceResponse])
def read_by_client(
    client_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_service_by_client_id(db, client_id)

@service_router.get("/get_services_by_day/{client_id}/{day_of_week}", response_model=List[ServiceResponse])
def read_services_by_day(
    client_id: int, 
    day_of_week: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_service_by_day_of_week(db, client_id, day_of_week)

@service_router.get("/get_services_by_visit_type/{client_id}/{visit_type}", response_model=List[ServiceResponse])
def read_services_by_visit_type(
    client_id: int, 
    visit_type: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_service_by_visit_type(db, client_id, visit_type)

@service_router.get("/get_all_services/", response_model=List[ServiceResponse])
def read_services(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_all_services(db, skip, limit)


@service_router.put("/update_service/{service_id}", response_model=ServiceResponse)
def update(
    service_id: int, 
    update_data: ServiceUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return update_service(db, service_id, update_data)

@service_router.delete("/delete_service/{service_id}")
def delete(
    service_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return delete_service(db, service_id)

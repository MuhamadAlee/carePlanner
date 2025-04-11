from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.visit import VisitCreate, VisitUpdate, VisitResponse, VisitClockedOUtUpdate, VisitCreateClockIn
from config.parameters import *
from config.database import get_db, engine, Base
from controllers.visit import (
    create_visit, get_visit, update_visit, 
    delete_visit, get_all_visits, get_visit_by_client_id,
    get_visit_by_roster_id, get_visit_by_user_id, update_clockout_visit, create_visit_for_clockin,
    get_visit_by_client_id_and_date, get_visit_by_client_id_and_date_range,
    get_visit_by_user_id_and_date, get_visit_by_user_id_and_date_range,
    get_pending_visits_by_client_id_and_date_range, get_pending_visits_by_user_id_and_date_range,
    get_pending_visits_by_date_range, approve_visit, get_visits_with_missing_or_short_notes
)
from controllers.auth import get_current_user
from utils.authorization import is_supervisor, is_carer_required
from models.visit import Visit
from models.user import User
from typing import List
from datetime import date

# ---- Routes ----
visit_router = APIRouter(tags=["Visits"])
Base.metadata.create_all(bind=engine)

@visit_router.post("/create_visit/", response_model=VisitResponse)
def create(
    visit_data: VisitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return create_visit(db, current_user.user_id, current_user.role_id, visit_data)

@visit_router.post("/clockIn/", response_model=VisitResponse)
def create_clock_in(
    visit_data: VisitCreateClockIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_carer_required)
):
    visit_data.status = CLOCKEDIN
    return create_visit_for_clockin(db, current_user.role_id, visit_data, current_user.user_id)

@visit_router.post("/clockOut/{visit_id}", response_model=VisitResponse)
def create_clock_out(
    visit_id: int,
    update_data: VisitClockedOUtUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_carer_required)
):
    update_data.status = ClOCKEDOUT
    return update_clockout_visit(db, current_user.user_id, current_user.role_id, visit_id, update_data)
    
@visit_router.get("/get_single_visit/{visit_id}", response_model=VisitResponse)
def read(
    visit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_carer_required)
):
    return get_visit(db, current_user.user_id, current_user.role_id, visit_id)

@visit_router.get("/get_single_visit_by_client/{client_id}", response_model=List[VisitResponse])
def read_by_client_id(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_carer_required)
):
    return get_visit_by_client_id(db, current_user.user_id, current_user.role_id, client_id)

@visit_router.get("/get_single_visit_by_roster_rota/{roster_id}", response_model=List[VisitResponse])
def read_by_rota_id(
    roster_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_carer_required)
):
    return get_visit_by_roster_id(db, current_user.user_id, current_user.role_id, roster_id)

@visit_router.get("/get_single_visit_by_user/{user_id}", response_model=List[VisitResponse])
def read_by_user_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_visit_by_user_id(db, user_id)

@visit_router.get("/get_visit_by_client_and_date/{client_id}/{visit_date}", response_model=List[VisitResponse])
def read_by_client_and_date(
    client_id: int,
    visit_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_carer_required)
):
    return get_visit_by_client_id_and_date(db, current_user.user_id, current_user.role_id, client_id, visit_date)

@visit_router.get("/get_visit_by_user_and_date/{user_id}/{visit_date}", response_model=List[VisitResponse])
def read_by_user_and_date(
    user_id: int,
    visit_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_visit_by_user_id_and_date(db, user_id, visit_date)

@visit_router.get("/get_visit_by_client_and_date_range/{client_id}/{start_date}/{end_date}", response_model=List[VisitResponse])
def read_by_client_and_date_range(
    client_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_carer_required)
):
    return get_visit_by_client_id_and_date_range(db, current_user.user_id, current_user.role_id, client_id, start_date, end_date)

@visit_router.get("/get_visit_by_user_and_date_range/{user_id}/{start_date}/{end_date}", response_model=List[VisitResponse])
def read_by_user_and_date_range(
    user_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_visit_by_user_id_and_date_range(db, user_id, start_date, end_date)

@visit_router.get("/get_all_visits/", response_model=List[VisitResponse])
def read_visits(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_carer_required)
):
    return get_all_visits(db, current_user.user_id, current_user.role_id, skip, limit)

@visit_router.put("/update_visit/{visit_id}", response_model=VisitResponse)
def update(
    visit_id: int,
    update_data: VisitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return update_visit(db, visit_id, update_data)

@visit_router.delete("/delete_visit/{visit_id}")
def delete(
    visit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return delete_visit(db, visit_id)


@visit_router.get("/get_pending_visits_by_user_and_date_range/{user_id}/{start_date}/{end_date}", response_model=List[VisitResponse])
def read_pending_by_user_and_date_range(
    user_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_pending_visits_by_user_id_and_date_range(db, user_id, start_date, end_date)

@visit_router.get("/get_pending_visits_by_client_and_date_range/{client_id}/{start_date}/{end_date}", response_model=List[VisitResponse])
def read_pending_by_client_and_date_range(
    client_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_pending_visits_by_client_id_and_date_range(db, client_id, start_date, end_date)


@visit_router.get("/get_pending_visits_by_date_range/{start_date}/{end_date}", response_model=List[VisitResponse])
def read_pending_by_date_range(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_pending_visits_by_date_range(db, start_date, end_date)

@visit_router.put("/approve_visit/{visit_id}", response_model=VisitResponse)
def approve_visit_by_id(
    visit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return approve_visit(db, visit_id)

@visit_router.get("/get_visits_with_short_notes", response_model=List[VisitResponse])
def read_visits_with_short_notes(
    min_length: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _ = Depends(is_supervisor)
):
    return get_visits_with_missing_or_short_notes(db)




from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from sqlalchemy import text
from schemas.roster import RosterCreate, RosterUpdate, RosterResponse
from config.database import get_db, engine, Base
from controllers.roster import (
    create_roster, get_roster, update_roster, delete_roster, 
    get_all_rosters, get_roster_by_client_id, 
    get_roster_by_user_id, get_roster_by_rota_id
)
from controllers.auth import get_current_user
from utils.authorization import is_supervisor, is_carer_required
from models.user import User
from scheduling.schdule_rota import schedule

# ---- Routes ----
roster_router = APIRouter(tags=["Rosters"])
Base.metadata.create_all(bind=engine)

@roster_router.post("/create_schedule/{first_day_of_month}/", response_model=dict)
def create(
    background_tasks: BackgroundTasks,
    first_day_of_month: date,
    _: User = Depends(is_supervisor),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
    background_tasks.add_task(schedule, tenant, first_day_of_month)
    return {"message": "Schedule creation started in the background"}

@roster_router.post("/create_roster/", response_model=RosterResponse)
def create_roster_route(
    roster_data: RosterCreate,
    _: User = Depends(is_supervisor),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_roster(db, roster_data)

@roster_router.get("/get_single_roster/{roster_id}/", response_model=RosterResponse)
def read(
    roster_id: int,
    _: User = Depends(is_carer_required),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_roster(db, current_user.user_id, current_user.role_id, roster_id)

@roster_router.get("/get_single_roster_by_client_id/{client_id}/{first_day_of_month}/", response_model=List[RosterResponse])
def read_by_client_id(
    client_id: int,
    first_day_of_month: date,
    _: User = Depends(is_carer_required),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_roster_by_client_id(db, current_user.user_id, current_user.role_id, client_id, first_day_of_month)

@roster_router.get("/get_single_roster_by_user_id/{user_id}/{first_day_of_month}/", response_model=List[RosterResponse])
def read_by_user_id(
    user_id: int,
    first_day_of_month: date,
    _: User = Depends(is_supervisor),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_roster_by_user_id(db, user_id, first_day_of_month)

@roster_router.get("/get_single_roster_by_rota_id/{rota_id}/{first_day_of_month}/", response_model=List[RosterResponse])
def read_by_rota_id(
    rota_id: int,
    first_day_of_month: date,
    _: User = Depends(is_carer_required),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_roster_by_rota_id(db, current_user.user_id, current_user.role_id, rota_id, first_day_of_month)

@roster_router.get("/get_all_rosters/{first_day_of_month}/", response_model=List[RosterResponse])
def read_rosters(
    first_day_of_month: date,
    skip: int = 0,
    limit: int = 10,
    _: User = Depends(is_carer_required),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_rosters(db, current_user.user_id, current_user.role_id, first_day_of_month, skip, limit)

@roster_router.put("/update_roster/{roster_id}", response_model=RosterResponse)
def update(
    roster_id: int,
    update_data: RosterUpdate,
    _: User = Depends(is_supervisor),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_roster(db, roster_id, update_data)

@roster_router.delete("/delete_roster/{roster_id}")
def delete(
    roster_id: int,
    _: User = Depends(is_supervisor),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_roster(db, current_user.user_id, current_user.role_id, roster_id)

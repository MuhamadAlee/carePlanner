from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.holiday import HolidayCreate, HolidayUpdate, HolidayResponse
from config.database import get_db, engine, Base
from controllers.holiday import (
    create_holiday, get_holiday, update_holiday, 
    delete_holiday, get_all_holidays, get_holiday_by_user_id
)
from controllers.auth import get_current_user
from utils.authorization import is_care_coordinator_required
from models.holiday import Holiday
from models.user import User
from typing import List

# ---- Routes ----
holiday_router = APIRouter(tags=["Holidays"])
Base.metadata.create_all(bind=engine)

@holiday_router.post("/create_holiday/", response_model=HolidayResponse, dependencies=[Depends(get_current_user)])
def create(holiday_data: HolidayCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_care_coordinator_required)):
    return create_holiday(db, holiday_data)
    
@holiday_router.get("/get_single_holiday/{holiday_id}", response_model=HolidayResponse, dependencies=[Depends(get_current_user)])
def read(holiday_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_care_coordinator_required)):
    return get_holiday(db, holiday_id)

@holiday_router.get("/get_single_holiday_by_user_id/{user_id}", response_model=List[HolidayResponse], dependencies=[Depends(get_current_user)])
def read_by_user_id(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_care_coordinator_required)):
    return get_holiday_by_user_id(db, user_id)

@holiday_router.get("/get_all_holidays/", response_model=List[HolidayResponse], dependencies=[Depends(get_current_user)])
def read_holidays(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_care_coordinator_required)):
    return get_all_holidays(db, skip, limit)

@holiday_router.put("/update_holiday/{holiday_id}", response_model=HolidayResponse, dependencies=[Depends(get_current_user)])
def update(holiday_id: int, update_data: HolidayUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_care_coordinator_required)):
    return update_holiday(db, holiday_id, update_data)

@holiday_router.delete("/delete_holiday/{holiday_id}", dependencies=[Depends(get_current_user)])
def delete(holiday_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_care_coordinator_required)):
    return delete_holiday(db, holiday_id)

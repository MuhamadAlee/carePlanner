from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.holidayQuota import HolidayQuotaCreate, HolidayQuotaUpdate, HolidayQuotaResponse
from config.database import get_db, engine, Base
from controllers.holidayQuota import (
    create_holiday_quota, get_holiday_quota, update_holiday_quota, 
    delete_holiday_quota, get_all_holiday_quotas,
    get_holiday_quota_by_user_id
)
from controllers.auth import get_current_user
from utils.authorization import is_care_coordinator_required
from models.holidayQuota import HolidayQuota
from models.user import User
from typing import List

# ---- Routes ----
holiday_quota_router = APIRouter(tags=["Holiday Quotas"])
Base.metadata.create_all(bind=engine)

@holiday_quota_router.post("/create_holiday_quota/", response_model=HolidayQuotaResponse, dependencies=[Depends(get_current_user)])
def create(holiday_quota_data: HolidayQuotaCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_care_coordinator_required)):
    return create_holiday_quota(db, holiday_quota_data)
    
@holiday_quota_router.get("/get_single_holiday_quota/{holiday_quota_id}", response_model=HolidayQuotaResponse, dependencies=[Depends(get_current_user)])
def read(holiday_quota_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_care_coordinator_required)):
    return get_holiday_quota(db, holiday_quota_id)

@holiday_quota_router.get("/get_single_holiday_quota_by_user_id/{user_id}", response_model=List[HolidayQuotaResponse], dependencies=[Depends(get_current_user)])
def read_by_user_id(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_care_coordinator_required)):
    return get_holiday_quota_by_user_id(db, user_id)

@holiday_quota_router.get("/get_all_holiday_quotas/", response_model=List[HolidayQuotaResponse], dependencies=[Depends(get_current_user)])
def read_holiday_quotas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_care_coordinator_required)):
    return get_all_holiday_quotas(db, skip, limit)

@holiday_quota_router.put("/update_holiday_quota/{holiday_quota_id}", response_model=HolidayQuotaResponse, dependencies=[Depends(get_current_user)])
def update(holiday_quota_id: int, update_data: HolidayQuotaUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_care_coordinator_required)):
    return update_holiday_quota(db, holiday_quota_id, update_data)

@holiday_quota_router.delete("/delete_holiday_quota/{holiday_quota_id}", dependencies=[Depends(get_current_user)])
def delete(holiday_quota_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_care_coordinator_required)):
    return delete_holiday_quota(db, holiday_quota_id)

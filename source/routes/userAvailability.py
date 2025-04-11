from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.userAvailability import UserAvailabilityCreate, UserAvailabilityUpdate, UserAvailabilityResponse
from controllers.userAvailability import (
    get_user_availability, get_single_user_availabilities, 
    get_all_users_availabilities, create_user_availability, 
    update_user_availability, delete_user_availability,
    get_single_user_availabilities_on_day
)
from config.database import get_db
from controllers.auth import get_current_user
from config.database import engine, Base, get_db, SessionLocal
from models.user import User
from utils.authorization import is_care_coordinator_required

# ---- Routes ----
availability_router = APIRouter(tags=["User Availability"])
Base.metadata.create_all(bind=engine)


@availability_router.post("/create_availability/", response_model=UserAvailabilityResponse, dependencies=[Depends(get_current_user)])
def create_availability(availability_data: UserAvailabilityCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user) , _=Depends(is_care_coordinator_required)):
    return create_user_availability(db, availability_data)

@availability_router.get("/get_availability/{availability_id}", response_model=UserAvailabilityResponse, dependencies=[Depends(get_current_user)])
def read_availability(availability_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user) , _=Depends(is_care_coordinator_required)):
    return get_user_availability(db, availability_id)

@availability_router.get("/get_user_availability/{user_id}", response_model=List[UserAvailabilityResponse], dependencies=[Depends(get_current_user)])
def read_user_availabilities(user_id:int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user) , _=Depends(is_care_coordinator_required)):
    return get_single_user_availabilities(db, user_id)

@availability_router.get("/get_user_availability_on_day/{user_id}/day", response_model=UserAvailabilityResponse, dependencies=[Depends(get_current_user)])
def read_user_availabilities(user_id:int,day:str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user) , _=Depends(is_care_coordinator_required)):
    return get_single_user_availabilities_on_day(db, user_id,day)

@availability_router.get("/get_all_users_availabilities/", response_model=List[UserAvailabilityResponse], dependencies=[Depends(get_current_user)])
def read_all_availabilities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user) , _=Depends(is_care_coordinator_required)):
    return get_all_users_availabilities(db, skip, limit)


@availability_router.put("/update_availability/{availability_id}", response_model=UserAvailabilityResponse, dependencies=[Depends(get_current_user)])
def update_availability(availability_id: int, update_data: UserAvailabilityUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user) , _=Depends(is_care_coordinator_required)):
    return update_user_availability(db, availability_id, update_data)

@availability_router.delete("/delete_availability/{availability_id}", dependencies=[Depends(get_current_user)])
def delete_availability(availability_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user) , _=Depends(is_care_coordinator_required)):
    return delete_user_availability(db, availability_id)

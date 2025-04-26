from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.payroll import PayrollCreate, PayrollUpdate, PayrollResponse
from config.database import get_db, engine, Base
from controllers.payroll import (
    create_payroll, get_payroll, update_payroll, 
    delete_payroll, get_all_payrolls,
    get_payroll_by_user_id, get_payroll_by_month
)
from controllers.auth import get_current_user
from utils.authorization import is_admin_required, is_yourself
from models.payroll import Payroll
from models.user import User
from typing import List
from fastapi import BackgroundTasks
from scheduling.generate_payroll import generate
from typing import List, Optional
from datetime import date, datetime
from config.parameters import WORK_HOURS, TIME_BASED

# ---- Routes ----
payroll_router = APIRouter(tags=["Payroll"])
Base.metadata.create_all(bind=engine)

from fastapi import Query

@payroll_router.post("/generate_payrolls", response_model=dict, dependencies=[Depends(get_current_user)])
def create_payrolls(
    background_tasks: BackgroundTasks,
    hours_type: str = Query(WORK_HOURS, description="Type of hours"),
    travel_type: str = Query(TIME_BASED, description="Type of travel"),
    first_day_of_month: date = Query(datetime.today().replace(day=1).date(), description="First day of the month"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
    background_tasks.add_task(generate, tenant, current_user, hours_type, travel_type , first_day_of_month)
    return {"message": "Payroll creation started in the background"}

@payroll_router.post("/create_payroll/", response_model=PayrollResponse, dependencies=[Depends(get_current_user)])
def create(payroll_data: PayrollCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_admin_required)):
    return create_payroll(db, payroll_data)
    
@payroll_router.get("/get_single_payroll/{payroll_id}", response_model=PayrollResponse, dependencies=[Depends(get_current_user)])
def read(payroll_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_admin_required)):
    return get_payroll(db, payroll_id)

@payroll_router.get("/get_single_payroll_by_user_id/{user_id}", response_model=List[PayrollResponse], dependencies=[Depends(get_current_user)])
def read_by_user_id(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_admin_required)):
    return get_payroll_by_user_id(db, user_id)

@payroll_router.get("/get_payroll_by_month/{user_id}/{payroll_date}", response_model=List[PayrollResponse], dependencies=[Depends(get_current_user)])
def read_payroll_by_month(
    user_id: int, 
    payroll_date: date ,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _=Depends(is_admin_required)
):
    """Fetch payroll records for a specific month based on a provided date (or defaults to the current month)."""
    return get_payroll_by_month(db, user_id, payroll_date)


@payroll_router.get("/get_payroll_by_month/{payroll_date}", response_model=List[PayrollResponse], dependencies=[Depends(get_current_user)])
def read_payroll_by_month( 
    payroll_date: date ,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _=Depends(is_yourself)
):
    """Fetch payroll records for a specific month based on a provided date (or defaults to the current month)."""
    return get_payroll_by_month(db, current_user.user_id, payroll_date)


@payroll_router.get("/get_all_payrolls/", response_model=List[PayrollResponse], dependencies=[Depends(get_current_user)])
def read_payrolls(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_admin_required)):
    return get_all_payrolls(db, skip, limit)

@payroll_router.put("/update_payroll/{payroll_id}", response_model=PayrollResponse, dependencies=[Depends(get_current_user)])
def update(payroll_id: int, update_data: PayrollUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_admin_required)):
    return update_payroll(db, payroll_id, update_data)

@payroll_router.delete("/delete_payroll/{payroll_id}", dependencies=[Depends(get_current_user)])
def delete(payroll_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_admin_required)):
    return delete_payroll(db, payroll_id)
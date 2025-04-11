from pydantic import BaseModel
from datetime import date
from typing import Optional

class PayrollBase(BaseModel):
    payroll_id: int
    user_id: int
    calls_entertained: int
    start_date: date
    end_date: date
    total_milage: float
    total_hours_travelled: float
    total_hours_worked: float
    grand_total: float

class PayrollCreate(BaseModel):
    user_id: int
    calls_entertained: int
    start_date: date
    end_date: date
    total_milage: float
    total_hours_travelled: float
    total_hours_worked: float
    grand_total: float

class PayrollUpdate(BaseModel):
    user_id: int
    calls_entertained: int
    start_date: date
    end_date: date
    total_milage: float
    total_hours_travelled: float
    total_hours_worked: float
    grand_total: float

class PayrollResponse(PayrollBase):
    payroll_id: int

    class Config:
        from_attributes = True

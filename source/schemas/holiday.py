from pydantic import BaseModel
from datetime import date
from typing import Optional

class HolidayBase(BaseModel):
    holiday_id: int
    user_id: int
    start_date: date
    end_date: date
    type: str  # Casual, Annual, Medical
    reason: Optional[str] = None

class HolidayCreate(BaseModel):
    user_id: int
    start_date: date
    end_date: date
    type: str  # Casual, Annual, Medical
    reason: Optional[str] = None

class HolidayUpdate(BaseModel):
    user_id: int
    start_date: date
    end_date: date
    type: str  # Casual, Annual, Medical
    reason: Optional[str] = None

class HolidayResponse(HolidayBase):
    holiday_id: int

    class Config:
        from_attributes = True

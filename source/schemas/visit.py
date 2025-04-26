from datetime import datetime, date, time
from pydantic import BaseModel
from typing import Optional
from config.parameters import VISIT_REVIEW_PENDING

# ---- Schemas ----

# ---- Address Model ----
class Address(BaseModel):
    line1: str                      # Most important
    line2: Optional[str] = None         # Optional
    postcode: str                       # Most important
    city: str
    county: Optional[str] = None        # Optional
    country: str = "UK"  

class VisitBase(BaseModel):
    roster_id: int
    user_id: Optional[int]
    client_id: int
    date: date
    clock_in: Optional[time] = None
    clock_out: Optional[time] = None
    clock_in_location: Optional[Address] = None 
    clock_out_location: Optional[Address] = None 
    duration: Optional[float] = None
    notes: Optional[str] = None
    status: str

class VisitCreate(BaseModel):
    roster_id: int
    user_id: Optional[int]
    client_id: int
    date: date
    clock_in: Optional[time] = None
    clock_out: Optional[time] = None
    clock_in_location: Optional[Address] = None 
    clock_out_location: Optional[Address] = None 
    duration: Optional[float] = None
    notes: Optional[str] = None
    status: str

class VisitCreateClockIn(BaseModel):
    roster_id: int
    client_id: int
    date: date
    clock_in: Optional[time] = None
    duration: Optional[float] = None
    clock_in_location: Optional[Address] = None 
    notes: Optional[str] = None
    status: Optional[str] = VISIT_REVIEW_PENDING

class VisitUpdate(BaseModel):
    roster_id: Optional[int]
    user_id: Optional[int]
    client_id: Optional[int]
    date: Optional[date]
    clock_in: Optional[time]
    clock_out: Optional[time]
    duration: Optional[float]
    notes: Optional[str]
    status: Optional[str]

class VisitClockedOUtUpdate(BaseModel):
    clock_out: Optional[time]
    clock_out_location: Optional[Address] = None 
    duration: Optional[float]
    status: Optional[str] = VISIT_REVIEW_PENDING

class VisitResponse(VisitBase):
    visit_id: int

    class Config:
        from_attributes = True

from datetime import datetime, time
from pydantic import BaseModel
from typing import Optional

# ---- Schemas ----

class ServiceBase(BaseModel):
    client_id: Optional[int]
    day_of_week: str
    start_time: time
    end_time: time
    alert: bool = False
    visit_type: str
    staff_required: int
    special_notes: Optional[str] = None

class ServiceCreate(BaseModel):
    client_id: Optional[int]
    day_of_week: str
    start_time: time
    end_time: time
    alert: Optional[bool] = False
    visit_type: str
    staff_required: int
    special_notes: Optional[str] = None

class ServiceUpdate(BaseModel):
    client_id: Optional[int]
    day_of_week: Optional[str]
    start_time: Optional[time]
    end_time: Optional[time]
    alert: Optional[bool]
    visit_type: Optional[str]
    staff_required: Optional[int]
    special_notes: Optional[str]

class ServiceResponse(ServiceBase):
    service_id: int
    created_at: datetime

    class Config:
        from_attributes = True

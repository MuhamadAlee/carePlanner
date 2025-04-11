from datetime import time
from pydantic import BaseModel
from typing import Optional

# ---- Schemas ----
class UserAvailabilityBase(BaseModel):
    user_id: int
    day_of_week: str  # e.g., "Monday", "Tuesday"
    start_time: time
    end_time: time
    is_weekend: bool = False

class UserAvailabilityCreate(BaseModel):
    user_id: int
    day_of_week: str
    start_time: time
    end_time: time
    is_weekend: bool = False

class UserAvailabilityUpdate(BaseModel):
    day_of_week: Optional[str]
    start_time: Optional[time]
    end_time: Optional[time]
    is_weekend: Optional[bool]

class UserAvailabilityResponse(BaseModel):
    user_id: int
    day_of_week: str
    start_time: time
    end_time: time
    is_weekend: bool

    class Config:
        from_attributes = True

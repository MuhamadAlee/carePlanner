from datetime import datetime, time, date
from pydantic import BaseModel
from typing import Optional


# ---- Schemas ----
class RosterBase(BaseModel):
    roster_id: int
    client_id: int
    service_id: int
    user_id: int
    day: str
    start_time: time
    end_time: time
    date: date


class RosterCreate(BaseModel):
    client_id: int
    service_id: int
    user_id: int
    day: str
    start_time: time
    end_time: time
    date: date

class RosterUpdate(BaseModel):
    client_id: Optional[int]
    service_id: Optional[int]
    user_id: Optional[int]
    day: Optional[str]
    start_time: Optional[time]
    end_time: Optional[time]
    date: Optional[date]


class RosterResponse(RosterBase):
    roster_id: int

    class Config:
        from_attributes = True

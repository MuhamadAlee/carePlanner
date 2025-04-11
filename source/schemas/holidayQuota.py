from pydantic import BaseModel
from typing import Optional

# ---- Schemas ----

class HolidayQuotaBase(BaseModel):
    user_id: int
    holiday_type: str
    total_days: int
    used_days: Optional[int] = 0

class HolidayQuotaCreate(BaseModel):
    user_id: int
    holiday_type: str
    total_days: int
    used_days: Optional[int] = 0

class HolidayQuotaUpdate(BaseModel):
    user_id: Optional[int]
    holiday_type: Optional[str]
    total_days: Optional[int]
    used_days: Optional[int]

class HolidayQuotaResponse(HolidayQuotaBase):
    holiday_quota_id: int

    class Config:
        from_attributes = True

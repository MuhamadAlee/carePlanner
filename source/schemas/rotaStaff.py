from pydantic import BaseModel
from typing import Optional

class RotaStaffBase(BaseModel):
    rota_id: int
    user_id: int

class RotaStaffCreate(BaseModel):
    rota_id: int
    user_id: int

class RotaStaffUpdate(BaseModel):
    user_id: Optional[int] = None
    rota_id: Optional[int] = None

class RotaStaffResponse(RotaStaffBase):
    rota_staff_id: int

    class Config:
        from_attributes = True

class RotaStaff(RotaStaffResponse):
    pass

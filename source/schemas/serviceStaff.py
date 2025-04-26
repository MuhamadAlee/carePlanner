from pydantic import BaseModel
from typing import Optional

class ServiceStaffBase(BaseModel):
    service_id: int
    user_id: int

class ServiceStaffCreate(BaseModel):
    service_id: int
    user_id: int

class ServiceStaffUpdate(BaseModel):
    user_id: Optional[int] = None
    service_id: Optional[int] = None

class ServiceStaffResponse(ServiceStaffBase):
    service_staff_id: int

    class Config:
        from_attributes = True

class ServiceStaff(ServiceStaffResponse):
    pass

from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

# ---- Schemas ----
class UserBase(BaseModel):
    role_id: Optional[int]
    name: str
    email: EmailStr
    password: str
    contact: Optional[str] = None
    address: Optional[str] = None
    employee_type: Optional[str] = None  # Full-time, Part-time, etc.
    working_hours: Optional[int] = None
    working_hour_rate: Optional[int] = None
    travel_rate : Optional[int] =None
    is_active: bool = True
    dbs_status: bool = False

class UserCreate(BaseModel):
    role_id: Optional[int]
    name: str
    email: EmailStr
    password: str
    contact: Optional[str] = None
    address: Optional[str] = None
    employee_type: Optional[str] = None  # Full-time, Part-time, etc.
    working_hours: Optional[int] = None
    working_hour_rate: Optional[int] = None
    travel_rate : Optional[int] =None
    is_active: bool = True
    dbs_status: bool = False

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: str
    contact: Optional[str]
    address: Optional[str]
    employee_type: Optional[str]
    working_hours: Optional[int]
    working_hour_rate: Optional[int]
    travel_rate : Optional[int]
    is_active: Optional[bool]
    dbs_status: Optional[bool]
    role_id: Optional[int]

class UserResponse(BaseModel):
    user_id: Optional[int]
    role_id: Optional[int]
    name: str
    email: EmailStr
    contact: Optional[str] = None
    address: Optional[str] = None
    employee_type: Optional[str] = None  # Full-time, Part-time, etc.
    working_hours: Optional[int] = None
    working_hour_rate: Optional[int]
    travel_rate : Optional[int]
    is_active: bool = True
    dbs_status: bool = False
    created_at: datetime
    
    class Config:
        from_attributes = True

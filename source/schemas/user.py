from datetime import datetime
from pydantic import BaseModel, EmailStr
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional
from sqlalchemy import Column
from enum import Enum 

# ---- Enums ----
class EmployeeType(str, Enum):
    permanent = "Permanent"
    contract = "Contract"
    zero_hour = "Zero-Hour Contract"

# ---- Address Model ----
class Address(BaseModel):
    line1: str                      # Most important
    line2: Optional[str] = None         # Optional
    postcode: str                       # Most important
    city: str
    county: Optional[str] = None        # Optional
    country: str = "UK"                 # Default is UK

# ---- Schemas ----
class UserBase(BaseModel):
    role_id: Optional[int]
    name: str
    email: EmailStr
    password: str
    contact: Optional[str] = None
    address: Optional[Address] = None 
    employee_type: Optional[EmployeeType] = EmployeeType.permanent
    working_hours: Optional[int] = None
    working_hour_rate: Optional[int] = None
    travel_rate: Optional[int] = None
    is_active: bool = True
    dbs_status: bool = True



class UserCreate(BaseModel):
    role_id: Optional[int]
    name: str
    email: EmailStr
    password: str
    contact: Optional[str] = None
    address: Optional[Address] = None
    address: Optional[Address] = None 
    employee_type: Optional[EmployeeType] = EmployeeType.permanent
    working_hour_rate: Optional[int] = None
    travel_rate: Optional[int] = None
    is_active: bool = True
    dbs_status: bool = True

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: str
    contact: Optional[str]
    address: Optional[Address] = None 
    employee_type: Optional[EmployeeType] = EmployeeType.permanent
    working_hours: Optional[int]
    working_hour_rate: Optional[int]
    travel_rate: Optional[int]
    is_active: Optional[bool]
    dbs_status: Optional[bool]
    role_id: Optional[int]

class UserResponse(BaseModel):
    user_id: Optional[int]
    role_id: Optional[int]
    name: str
    email: EmailStr
    contact: Optional[str] = None
    address: Optional[Address] = None 
    employee_type: Optional[EmployeeType] = EmployeeType.permanent
    working_hours: Optional[int] = None
    working_hour_rate: Optional[int]
    travel_rate: Optional[int]
    is_active: bool = True
    dbs_status: bool = True
    created_at: datetime

    class Config:
        from_attributes = True

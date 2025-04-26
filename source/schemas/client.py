from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional



class Address(BaseModel):
    line1: str                           # Most important
    line2: Optional[str] = None         # Optional
    postcode: str                       # Most important
    city: str
    county: Optional[str] = None        # Optional
    country: str = "UK" 

# ---- Schemas ----
class ClientBase(BaseModel):
    name: str
    email: str
    dob: date
    contact: Optional[str] = None
    medical_info: Optional[str] = None
    dnr_status: bool = False
    service_start: Optional[date] = None
    service_end: Optional[date] = None
    care_plan: Optional[str] = None  # File path or URL to the document
    diagnosis: Optional[str] = None
    allergies: Optional[str] = None
    location: Optional[Address] = None
    charge_rate: Optional[int] = None
    is_active: bool = True

class ClientCreate(BaseModel):
    name: str
    email: str
    dob: date
    contact: Optional[str] = None
    medical_info: Optional[str] = None
    dnr_status: bool = False
    service_start: Optional[date] = None
    service_end: Optional[date] = None
    care_plan: Optional[str] = None  # File path or URL to the document
    diagnosis: Optional[str] = None
    allergies: Optional[str] = None
    location: Optional[Address] = None
    charge_rate: Optional[int] = None
    is_active: bool = True

class ClientUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    dob: Optional[date]
    contact: Optional[str]
    medical_info: Optional[str]
    dnr_status: Optional[bool]
    service_start: Optional[date]
    service_end: Optional[date]
    care_plan: Optional[str]  # File path update
    diagnosis: Optional[str]
    allergies: Optional[str]
    location: Optional[Address] = None
    charge_rate: Optional[int]
    is_active: Optional[bool]

class ClientResponse(ClientBase):
    client_id: int

    class Config:
        from_attributes = True

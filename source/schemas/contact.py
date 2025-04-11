from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# ---- Schemas ----
class ContactBase(BaseModel):
    client_id: Optional[int]
    name: str
    contact: str
    relation: Optional[str] = None

class ContactCreate(BaseModel):
    client_id: Optional[int]
    name: str
    contact: str
    relation: Optional[str] = None

class ContactUpdate(BaseModel):
    name: Optional[str]
    contact: Optional[str]
    relation: Optional[str]

class ContactResponse(ContactBase):
    contact_id: int
    client_id: Optional[int]
    
    class Config:
        from_attributes = True
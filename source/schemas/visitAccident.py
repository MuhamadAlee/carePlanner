from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# ---- Schemas ----

class VisitAccidentBase(BaseModel):
    visit_accident_id: int
    visit_id: int
    details: Optional[str] = None
    status: Optional[str] = None

class VisitAccidentCreate(BaseModel):
    visit_id: int
    details: Optional[str] = None
    status: Optional[str] = None

class VisitAccidentUpdate(BaseModel):
    visit_id: Optional[int] = None
    details: Optional[str] = None
    status: Optional[str] = None

class VisitAccidentResponse(VisitAccidentBase):
    visit_accident_id: int
    details: str
    status: str
    when: datetime

    class Config:
        from_attributes = True

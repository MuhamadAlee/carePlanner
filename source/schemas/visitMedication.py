from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# ---- Schemas ----

class VisitMedicationBase(BaseModel):
    visit_medication_id: int
    medication_id: int
    visit_id: int
    details: Optional[str] = None
    status: Optional[str] = None

class VisitMedicationCreate(BaseModel):
    medication_id: int
    visit_id: int
    details: Optional[str] = None
    status: Optional[str] = None

class VisitMedicationUpdate(BaseModel):
    medication_id: Optional[int] = None
    visit_id: Optional[int] = None
    details: Optional[str] = None
    status: Optional[str] = None

class VisitMedicationResponse(VisitMedicationBase):
    visit_medication_id: int

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional

class RotaMedicationBase(BaseModel):
    rota_id: int
    name: str
    dosage: str
    instructions: Optional[str] = None

class RotaMedicationCreate(BaseModel):
    rota_id: int
    name: str
    dosage: str
    instructions: Optional[str] = None

class RotaMedicationUpdate(BaseModel):
    rota_id: Optional[int] = None
    name: Optional[str] = None
    dosage: Optional[str] = None
    instructions: Optional[str] = None

class RotaMedicationResponse(RotaMedicationBase):
    medication_id: int
    
    class Config:
        from_attributes = True

class RotaMedication(RotaMedicationResponse):
    pass
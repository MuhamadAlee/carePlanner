from pydantic import BaseModel
from typing import Optional

class ServiceMedicationBase(BaseModel):
    service_id: int
    name: str
    dosage: str
    instructions: Optional[str] = None

class ServiceMedicationCreate(BaseModel):
    service_id: int
    name: str
    dosage: str
    instructions: Optional[str] = None

class ServiceMedicationUpdate(BaseModel):
    service_id: Optional[int] = None
    name: Optional[str] = None
    dosage: Optional[str] = None
    instructions: Optional[str] = None

class ServiceMedicationResponse(ServiceMedicationBase):
    medication_id: int
    
    class Config:
        from_attributes = True

class ServiceMedication(ServiceMedicationResponse):
    pass
from datetime import date
from pydantic import BaseModel
from typing import Optional

# ---- Schemas ----
class TrainingBase(BaseModel):
    user_id: int
    training_name: str
    training_status: str
    completion_date: date
    expiry_date: Optional[date] = None

class TrainingCreate(BaseModel):
    user_id: int
    training_name: str
    training_status: str
    completion_date: date
    expiry_date: Optional[date] = None

class TrainingUpdate(BaseModel):
    training_name: Optional[str]
    training_status: Optional[str]
    completion_date: Optional[date]
    expiry_date: Optional[date]

class TrainingResponse(TrainingBase):
    training_id: int
    
    class Config:
        from_attributes = True
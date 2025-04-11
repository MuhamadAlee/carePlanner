from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# ---- Schemas ----

class VisitTaskBase(BaseModel):
    visit_task_id: int
    task_id: int
    visit_id: int
    details: Optional[str] = None
    status: Optional[str] = None

class VisitTaskCreate(BaseModel):
    task_id: int
    visit_id: int
    details: Optional[str] = None
    status: Optional[str] = None

class VisitTaskUpdate(BaseModel):
    task_id: Optional[int] = None
    visit_id: Optional[int] = None
    details: Optional[str] = None
    status: Optional[str] = None

class VisitTaskResponse(VisitTaskBase):
    visit_task_id: int

    class Config:
        from_attributes = True

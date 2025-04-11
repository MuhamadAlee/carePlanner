from pydantic import BaseModel
from typing import Optional


class RotaTaskBase(BaseModel):
    rota_id: int
    description: Optional[str] = None
    priority: str  # High / Medium / Low


class RotaTaskCreate(BaseModel):
    rota_id: int
    description: Optional[str] = None
    priority: str  # High / Medium / Low


class RotaTaskUpdate(BaseModel):
    rota_id: Optional[int] = None
    description: Optional[str] = None
    priority: Optional[str] = None


class RotaTaskResponse(RotaTaskBase):
    task_id: int

    class Config:
        from_attributes = True


class RotaTask(RotaTaskResponse):
    pass

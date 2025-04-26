from pydantic import BaseModel
from typing import Optional


class ServiceTaskBase(BaseModel):
    service_id: int
    description: Optional[str] = None
    priority: str  # High / Medium / Low


class ServiceTaskCreate(BaseModel):
    service_id: int
    description: Optional[str] = None
    priority: str  # High / Medium / Low


class ServiceTaskUpdate(BaseModel):
    service_id: Optional[int] = None
    description: Optional[str] = None
    priority: Optional[str] = None


class ServiceTaskResponse(ServiceTaskBase):
    task_id: int

    class Config:
        from_attributes = True


class ServiceTask(ServiceTaskResponse):
    pass

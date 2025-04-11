
from uuid import uuid4
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

# ---- Schemas ----
class TenantBase(BaseModel):
    name: str
    slug: str
    email: EmailStr
    subscription_plan: str
    subscription_status: str

class TenantCreate(TenantBase):
    pass

class TenantUpdate(BaseModel):
    name: Optional[str]
    slug: Optional[str]
    email: Optional[EmailStr]
    subscription_plan: Optional[str]
    subscription_status: Optional[str]

class TenantResponse(TenantBase):
    tenant_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
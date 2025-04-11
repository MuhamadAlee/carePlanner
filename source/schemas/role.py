from datetime import datetime
from pydantic import BaseModel
from typing import Optional


# Base Schema
class RoleBase(BaseModel):
    role_name: str
    description: Optional[str] = None

# Create Schema
class RoleCreate(BaseModel):
    role_name: str
    description: Optional[str] = None

# Update Schema
class RoleUpdate(BaseModel):
    role_name: Optional[str]
    description: Optional[str]

# Response Schema
class RoleResponse(RoleBase):
    role_id: int
    role_name: str
    
    class Config:
        from_attributes = True

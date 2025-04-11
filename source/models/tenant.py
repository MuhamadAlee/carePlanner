from sqlalchemy import Column, Integer, String, Boolean
from datetime import datetime
from config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Boolean, Enum, ForeignKey, TIMESTAMP


# ---- Models ----
class Tenant(Base):
    __tablename__ = "tenants"
    
    tenant_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    subscription_plan = Column(String(50), nullable=False)
    subscription_status = Column(Enum("active", "pending", "expired", name="subscription_status"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)


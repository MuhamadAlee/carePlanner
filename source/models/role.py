from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP, UniqueConstraint
from datetime import datetime
from config.database import Base
from sqlalchemy.orm import relationship

class Role(Base):
    __tablename__ = "roles"
    
    role_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    users = relationship("User", back_populates="role", cascade="all, delete")

    __table_args__ = (UniqueConstraint('role_name', name='uq_role'),)

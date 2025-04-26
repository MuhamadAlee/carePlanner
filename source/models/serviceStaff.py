from sqlalchemy import Column, ForeignKey, Integer

from sqlalchemy.orm import relationship
from config.database import Base

class ServiceStaff(Base):
    __tablename__ = "service_staff"
    
    rota_staff_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"),nullable=True)
    service_id = Column(Integer, ForeignKey("services.service_id", ondelete="CASCADE"),nullable=True)
    
    user = relationship("User", back_populates="service_staff")
    service = relationship("Service", back_populates="service_staff")
    
   
    
    
    
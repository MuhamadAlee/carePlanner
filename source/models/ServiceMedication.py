from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from config.database import Base

class ServiceMedication(Base):
    __tablename__ = "service_medication"
    
    medication_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    service_id = Column(Integer, ForeignKey("services.service_id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    dosage = Column(String(100), nullable=False)
    instructions = Column(Text, nullable=True)
    
    service = relationship("Service", back_populates="service_medication")
    visit_medications = relationship("VisitMedication", back_populates="service_medication", cascade="all, delete")

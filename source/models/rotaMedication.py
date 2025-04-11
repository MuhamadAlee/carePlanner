from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from config.database import Base

class RotaMedication(Base):
    __tablename__ = "rota_medication"
    
    medication_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    rota_id = Column(Integer, ForeignKey("rotas.rota_id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    dosage = Column(String(100), nullable=False)
    instructions = Column(Text, nullable=True)
    
    rota = relationship("Rota", back_populates="rota_medication")
    visit_medications = relationship("VisitMedication", back_populates="rota_medication", cascade="all, delete")

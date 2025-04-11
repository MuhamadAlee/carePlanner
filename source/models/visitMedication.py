from sqlalchemy import Column, Integer, ForeignKey, Text
from config.database import Base
from sqlalchemy.orm import relationship

class VisitMedication(Base):
    __tablename__ = "visit_medications"
    
    visit_medication_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    visit_id = Column(Integer, ForeignKey("visits.visit_id", ondelete="CASCADE"), nullable=False)
    medication_id = Column(Integer, ForeignKey("rota_medication.medication_id", ondelete="CASCADE"), nullable=False)
    
    details = Column(Text, nullable=True)
    status = Column(Text, nullable=True)

    rota_medication = relationship("RotaMedication", back_populates="visit_medications")
    visit = relationship("Visit", back_populates="visit_medications")

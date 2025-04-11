from sqlalchemy import Column, Integer, ForeignKey, Text, TIMESTAMP
from config.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class VisitAccident(Base):
    __tablename__ = "visit_accidents"
    
    visit_accident_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    visit_id = Column(Integer, ForeignKey("visits.visit_id", ondelete="CASCADE"), nullable=False)
    when = Column(TIMESTAMP, default=datetime.utcnow)
    
    details = Column(Text, nullable=True)
    status = Column(Text, nullable=True)

    visit = relationship("Visit", back_populates="visit_accidents")

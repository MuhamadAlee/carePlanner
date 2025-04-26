from sqlalchemy import Column, String, ForeignKey, Text, DECIMAL, Date, TIMESTAMP, Integer, Time
from config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

class Visit(Base):
    __tablename__ = "visits"
    
    visit_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    roster_id = Column(Integer, ForeignKey("rosters.roster_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.client_id", ondelete="CASCADE"), nullable=False)
    
    date = Column(Date, nullable=False)
    clock_in = Column(Time, nullable=True)
    clock_out = Column(Time, nullable=True)
    clock_in_location = Column(JSONB, nullable=True)
    clock_out_location = Column(JSONB, nullable=True)
    duration = Column(DECIMAL(5,2), nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(String(50), nullable=False)
    
    roster = relationship("Roster", back_populates="visits")
    user = relationship("User", back_populates="visits")
    client = relationship("Client", back_populates="visits")
    visit_tasks = relationship("VisitTask", back_populates="visit", cascade="all, delete")
    visit_medications = relationship("VisitMedication", back_populates="visit", cascade="all, delete")
    visit_accidents = relationship("VisitAccident", back_populates="visit", cascade="all, delete")

    

from sqlalchemy import Column, String, ForeignKey, Text, Integer, Time, Boolean, TIMESTAMP
from config.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Rota(Base):
    __tablename__ = "rotas"
    
    rota_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    client_id = Column(Integer,ForeignKey("clients.client_id", ondelete="SET NULL"), nullable=True)
    
    day_of_week = Column(Text, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    alert = Column(Boolean, default=False, nullable=False)
    visit_type = Column(String(100), nullable=False)
    staff_required = Column(Integer, nullable=False)
    special_notes = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    client = relationship("Client", back_populates="rotas")
    rota_staff = relationship("RotaStaff", back_populates="rota", cascade="all, delete")
    rota_task = relationship("RotaTask", back_populates="rota", cascade="all, delete")
    rota_medication = relationship("RotaMedication", back_populates="rota", cascade="all, delete")
    rosters = relationship("Roster", back_populates="rota", cascade="all, delete")

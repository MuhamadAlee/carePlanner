from sqlalchemy import Column, String, ForeignKey, Text, Integer, Time, Date
from config.database import Base
from sqlalchemy.orm import relationship
from datetime import date

class Roster(Base):
    __tablename__ = "rosters"
    
    roster_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.client_id", ondelete="CASCADE"), nullable=False)
    rota_id = Column(Integer, ForeignKey("rotas.rota_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    
    day = Column(Text, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    date = Column(Date, nullable=False)
    
    client = relationship("Client", back_populates="rosters")
    rota = relationship("Rota", back_populates="rosters")
    user = relationship("User", back_populates="rosters")
    visits = relationship("Visit", back_populates="roster", cascade="all, delete")
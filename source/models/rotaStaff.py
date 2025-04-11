from sqlalchemy import Column, ForeignKey, Integer

from sqlalchemy.orm import relationship
from config.database import Base

class RotaStaff(Base):
    __tablename__ = "rota_staff"
    
    rota_staff_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"),nullable=True)
    rota_id = Column(Integer, ForeignKey("rotas.rota_id", ondelete="CASCADE"),nullable=True)
    
    user = relationship("User", back_populates="rota_staff")
    rota = relationship("Rota", back_populates="rota_staff")
    
   
    
    
    
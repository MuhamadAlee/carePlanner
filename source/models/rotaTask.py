from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from config.database import Base

class RotaTask(Base):
    __tablename__ = "rota_task"
    
    task_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rota_id = Column(Integer, ForeignKey("rotas.rota_id", ondelete="CASCADE"), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(50), nullable=False)  # High / Medium / Low
    
    rota = relationship("Rota", back_populates="rota_task")
    visit_tasks = relationship("VisitTask", back_populates="rota_task", cascade="all, delete")
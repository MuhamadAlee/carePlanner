from sqlalchemy import Column, Integer, ForeignKey, Text
from config.database import Base
from sqlalchemy.orm import relationship

class VisitTask(Base):
    __tablename__ = "visit_tasks"
    
    visit_task_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    
    visit_id = Column(Integer, ForeignKey("visits.visit_id", ondelete="CASCADE"), nullable=False)
    task_id = Column(Integer, ForeignKey("rota_task.task_id", ondelete="CASCADE"), nullable=False)
    
    details = Column(Text, nullable=True)
    status = Column(Text, nullable=True)

    rota_task = relationship("RotaTask", back_populates="visit_tasks")
    visit = relationship("Visit", back_populates="visit_tasks")

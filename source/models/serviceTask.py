from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from config.database import Base

class ServiceTask(Base):
    __tablename__ = "service_task"
    
    task_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    service_id = Column(Integer, ForeignKey("services.service_id", ondelete="CASCADE"), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(50), nullable=False)  # High / Medium / Low
    
    service = relationship("Service", back_populates="service_task")
    visit_tasks = relationship("VisitTask", back_populates="service_task", cascade="all, delete")
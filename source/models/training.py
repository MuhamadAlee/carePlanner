from sqlalchemy import Column, String, Date, ForeignKey, Integer
from config.database import Base
from sqlalchemy.orm import relationship

class Training(Base):
    __tablename__ = "trainings"
    
    training_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    
    training_status = Column(String(255), nullable=False)
    training_name = Column(String(255), nullable=False)
    completion_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=True)
    
    user = relationship("User", back_populates="trainings")
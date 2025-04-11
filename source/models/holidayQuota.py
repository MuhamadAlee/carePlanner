from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class HolidayQuota(Base):
    __tablename__ = "holiday_quotas"

    holiday_quota_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    holiday_type = Column(String(50), nullable=False)  # e.g., Casual, Annual, Medical
    total_days = Column(Integer, nullable=False)  # Allowed leave quota
    used_days = Column(Integer, default=0)  # Days already used

    user = relationship("User", back_populates="holiday_quotas")

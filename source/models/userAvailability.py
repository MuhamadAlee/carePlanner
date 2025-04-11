from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Time, UniqueConstraint
from config.database import Base
from sqlalchemy.orm import relationship

class UserAvailability(Base):
    __tablename__ = "user_availability"

    availability_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    day_of_week = Column(String(20), nullable=False)  # Monday, Tuesday, etc.
    start_time = Column(Time, nullable=False)  # e.g., 07:00:00 for 7 AM
    end_time = Column(Time, nullable=False)  # e.g., 17:00:00 for 5 PM
    is_weekend = Column(Boolean, default=False)  # True if it's for weekends

    user = relationship("User", back_populates="user_availability")

    __table_args__ = (UniqueConstraint("user_id", "day_of_week", name="uq_user_day"),)

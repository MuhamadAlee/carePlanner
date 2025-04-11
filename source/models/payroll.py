from sqlalchemy import Column, Integer, Date, ForeignKey, Double
from sqlalchemy.orm import relationship
from config.database import Base

class Payroll(Base):
    __tablename__ = "payrolls"

    payroll_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    calls_entertained = Column(Integer, nullable=False, default=0)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_milage = Column(Double, nullable=False, default=0)
    total_hours_travelled = Column(Double, nullable=False, default=0)
    total_hours_worked = Column(Double, nullable=False, default=0)
    grand_total = Column(Double, nullable=False, default=0.0)

    user = relationship("User", back_populates="payrolls")
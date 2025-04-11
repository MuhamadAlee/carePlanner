from sqlalchemy import Column, String, Boolean, Enum, ForeignKey, TIMESTAMP, Integer
from datetime import datetime
from config.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.role_id", ondelete="SET NULL"), nullable=True)
    
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    contact = Column(String(20), nullable=True)
    address = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    employee_type = Column(String(20), nullable=True)  # Full-time, Part-time, etc.
    working_hours = Column(Integer, nullable=True)
    working_hour_rate = Column(Integer, nullable=True)
    travel_rate = Column(Integer, nullable=True)
    
    is_active = Column(Boolean, default=True)
    dbs_status = Column(Boolean, default=False)  # Background check status
    
    role = relationship("Role", back_populates="users")
    trainings = relationship("Training", back_populates="user", cascade="all, delete") 
    rota_staff = relationship("RotaStaff", back_populates="user", cascade="all, delete")
    visits = relationship("Visit", back_populates="user", cascade="all, delete")
    holiday_quotas = relationship("HolidayQuota", back_populates="user", cascade="all, delete")
    holidays = relationship("Holiday", back_populates="user", cascade="all, delete")
    payrolls = relationship("Payroll", back_populates="user", cascade="all, delete")
    rosters = relationship("Roster", back_populates="user", cascade="all, delete")
    user_availability = relationship("UserAvailability", back_populates="user", cascade="all, delete")



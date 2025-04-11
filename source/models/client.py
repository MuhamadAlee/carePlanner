from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from config.database import Base

class Client(Base):
    __tablename__ = "clients"
    

    client_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    dob = Column(Date, nullable=True)
    contact = Column(String(20), nullable=True)
    medical_info = Column(Text, nullable=True)
    dnr_status = Column(Boolean, default=False)
    service_start = Column(Date, nullable=True)
    service_end = Column(Date, nullable=True)
    care_plan = Column(String, nullable=True)  # Path to the uploaded file
    diagnosis = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    location = Column(Text, nullable=True)
    charge_rate = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)

    contacts = relationship("Contact", back_populates="client", cascade="all, delete")
    rosters = relationship("Roster", back_populates="client", cascade="all, delete")
    rotas = relationship("Rota", back_populates="client", cascade="all, delete")
    visits = relationship("Visit", back_populates="client", cascade="all, delete")
    invoices = relationship("Invoice", back_populates="client", cascade="all, delete")

from sqlalchemy import Column, String, ForeignKey, Integer, Date
from sqlalchemy.orm import relationship
from config.database import Base

class Invoice(Base):
    __tablename__ = "invoices"
    
    invoice_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    client_id= Column(Integer, ForeignKey("clients.client_id", ondelete="SET NULL"), nullable=True)
    
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    authority = Column(String(255), nullable=False)
    billable_amount = Column(Integer, nullable=False)
    payment_status = Column(String(50), nullable=False)
    
    client = relationship("Client", back_populates="invoices")
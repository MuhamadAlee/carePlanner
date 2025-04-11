from sqlalchemy import Column, String, ForeignKey, Text, Integer
from config.database import Base
from sqlalchemy.orm import relationship

class Contact(Base):
    __tablename__ = "contacts"
    
    contact_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.client_id", ondelete="SET NULL"), nullable=True)
    
    name = Column(String(100), nullable=False)
    contact = Column(String(100), nullable=False)
    relation = Column(Text, nullable=True)
    
    client = relationship("Client", back_populates="contacts")

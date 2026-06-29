from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime
import uuid

from ..db.base import Base

class ObligationEntity(Base):
    __tablename__ = "obligations"
    
    obligation_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    contract_id = Column(String(36), ForeignKey("contracts.contract_id"), nullable=False)
    text = Column(Text, nullable=False)
    deadline = Column(DateTime, nullable=True)
    regulation = Column(String(200), nullable=True)
    priority = Column(String(20), nullable=False, default="medium")  # critical, high, medium, low
    status = Column(String(20), nullable=False, default="open")  # open, in_progress, completed
    assigned_to = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    contract = relationship("ContractEntity", back_populates="obligations")

class ObligationModel(BaseModel):
    obligation_id: str = None
    contract_id: str
    text: str
    deadline: datetime = None
    regulation: str = None
    priority: str = "medium"
    status: str = "open"
    assigned_to: str = None
    created_at: datetime = None
    updated_at: datetime = None
    
    class Config:
        from_attributes = True

class ObligationCreate(BaseModel):
    text: str
    deadline: datetime = None
    regulation: str = None
    priority: str = "medium"
    assigned_to: str = None

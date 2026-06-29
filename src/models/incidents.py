from sqlalchemy import Column, String, Text, DateTime
from pydantic import BaseModel
from datetime import datetime
import uuid

from ..db.base import Base

class IncidentEntity(Base):
    __tablename__ = "incidents"
    
    incident_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False)
    severity = Column(String(20), nullable=False)  # critical, high, medium, low
    status = Column(String(20), nullable=False, default="open")  # open, investigating, resolved
    related_obligations = Column(Text, nullable=True)  # JSON list of obligation_ids
    remediation_status = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class IncidentModel(BaseModel):
    incident_id: str = None
    title: str
    description: str
    date: datetime
    severity: str
    status: str = "open"
    related_obligations: list = None
    remediation_status: str = None
    created_at: datetime = None
    updated_at: datetime = None
    
    class Config:
        from_attributes = True

class IncidentCreate(BaseModel):
    title: str
    description: str
    date: datetime
    severity: str
    related_obligations: list = None

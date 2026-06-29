import uuid
from sqlalchemy import Column, String, Text, DateTime, Integer
from .base import Base
from datetime import datetime
from pydantic import BaseModel



class IncidentEntity(Base):
    __tablename__ = "incidents"
    
    incident_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255))
    description = Column(Text)
    severity = Column(String(16))
    status = Column(String(32), default="open")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

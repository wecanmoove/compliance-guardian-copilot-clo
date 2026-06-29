from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.orm import declarative_base
from datetime import datetime
from pydantic import BaseModel

Base = declarative_base()


class IncidentEntity(Base):
    __tablename__ = "incidents"
    
    incident_id = Column(String(36), primary_key=True)
    title = Column(String(255))
    description = Column(Text)
    severity = Column(String(16))
    status = Column(String(32), default="open")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

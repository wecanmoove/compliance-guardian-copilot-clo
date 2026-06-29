from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime
import uuid

from ..db.base import Base

class ComplianceGapEntity(Base):
    __tablename__ = "compliance_gaps"
    
    gap_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    obligation_id = Column(String(36), ForeignKey("obligations.obligation_id"), nullable=False)
    status = Column(String(20), nullable=False, default="open")  # open, in_progress, closed
    target_date = Column(DateTime, nullable=True)
    owner = Column(String(200), nullable=True)
    evidence_links = Column(Text, nullable=True)
    remediation_plan = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ComplianceGapModel(BaseModel):
    gap_id: str = None
    obligation_id: str
    status: str = "open"
    target_date: datetime = None
    owner: str = None
    evidence_links: str = None
    remediation_plan: str = None
    created_at: datetime = None
    updated_at: datetime = None
    
    class Config:
        from_attributes = True

class ComplianceGapCreate(BaseModel):
    obligation_id: str
    target_date: datetime = None
    owner: str = None
    remediation_plan: str = None

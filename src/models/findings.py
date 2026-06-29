from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime
import uuid

from ..db.base import Base
from .contracts import RiskLevel

class RiskFindingEntity(Base):
    __tablename__ = "risk_findings"
    
    finding_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    contract_id = Column(String(36), ForeignKey("contracts.contract_id"), nullable=False)
    clause_reference = Column(String(500), nullable=True)
    description = Column(Text, nullable=False)
    level = Column(String(20), nullable=False)
    recommendation = Column(Text, nullable=False)
    evidence = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    contract = relationship("ContractEntity", back_populates="findings")

class RiskFindingModel(BaseModel):
    finding_id: str = None
    contract_id: str
    clause_reference: str = None
    description: str
    level: str  # critical, high, medium, low
    recommendation: str
    evidence: str = None
    created_at: datetime = None
    
    class Config:
        from_attributes = True

class RiskFindingCreate(BaseModel):
    clause_reference: str = None
    description: str
    level: str
    recommendation: str
    evidence: str = None

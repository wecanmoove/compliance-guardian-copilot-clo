import uuid
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from .base import Base
from datetime import datetime
from pydantic import BaseModel



class RiskFindingEntity(Base):
    __tablename__ = "findings"
    
    finding_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    contract_id = Column(String(36), ForeignKey("contracts.contract_id"))
    clause_reference = Column(String(255))
    description = Column(Text)
    level = Column(String(16))
    recommendation = Column(Text)
    evidence = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class RiskFindingModel(BaseModel):
    finding_id: str
    contract_id: str
    clause_reference: str
    description: str
    level: str
    recommendation: str
    evidence: str
    
    class Config:
        from_attributes = True

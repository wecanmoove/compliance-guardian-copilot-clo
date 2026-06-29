import uuid
from sqlalchemy import Column, String, Integer, Text, DateTime, Enum
from .base import Base
from datetime import datetime
from pydantic import BaseModel
from enum import Enum as PyEnum



class RiskLevel(str, PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ContractEntity(Base):
    __tablename__ = "contracts"
    
    contract_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    file_name = Column(String(255), nullable=False)
    business_owner = Column(String(255))
    department = Column(String(255))
    file_path = Column(String(500))
    extracted_text = Column(Text)
    highest_risk_level = Column(String(16), default="low")
    summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ContractModel(BaseModel):
    contract_id: str
    file_name: str
    business_owner: str
    department: str
    highest_risk_level: str
    summary: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ContractSummary(BaseModel):
    contract_id: str
    file_name: str
    business_owner: str
    highest_risk_level: str
    created_at: datetime
    
    class Config:
        from_attributes = True

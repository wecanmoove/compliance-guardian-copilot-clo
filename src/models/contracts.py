from sqlalchemy import Column, String, DateTime, Text, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
import uuid

from ..db.base import Base

class RiskLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ContractEntity(Base):
    __tablename__ = "contracts"
    
    contract_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    file_name = Column(String(500), nullable=False)
    business_owner = Column(String(200), nullable=True)
    department = Column(String(200), nullable=True)
    highest_risk_level = Column(SQLEnum(RiskLevel), nullable=True)
    summary = Column(Text, nullable=True)
    extracted_text = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tenant_id = Column(String(36), nullable=False, default="default")
    
    # Relationships
    findings = relationship("RiskFindingEntity", back_populates="contract", cascade="all, delete-orphan")
    obligations = relationship("ObligationEntity", back_populates="contract", cascade="all, delete-orphan")

class ContractUploadRequest(BaseModel):
    file_name: str = Field(..., max_length=500)
    business_owner: str = Field(..., max_length=200)
    department: str = Field(..., max_length=200)

class ContractModel(BaseModel):
    contract_id: str
    file_name: str
    business_owner: str
    department: str
    highest_risk_level: RiskLevel = None
    summary: str = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ContractSummary(BaseModel):
    contract_id: str
    file_name: str
    business_owner: str
    department: str
    highest_risk_level: RiskLevel = None
    created_at: datetime

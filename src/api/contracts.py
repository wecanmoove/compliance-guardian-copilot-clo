from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
import os

from ..db import get_db
from ..models.contracts import (
    ContractEntity, ContractModel, ContractUploadRequest, 
    ContractSummary, RiskLevel
)
from ..models.findings import RiskFindingEntity, RiskFindingModel
from ..config import settings

router = APIRouter(prefix="/api/contracts", tags=["contracts"])

@router.post("/upload", response_model=ContractModel)
async def upload_contract(
    file: UploadFile = File(...),
    business_owner: str = None,
    department: str = None,
    db: Session = Depends(get_db)
):
    """Upload a contract for analysis"""
    try:
        # Save file
        os.makedirs(settings.STORAGE_PATH, exist_ok=True)
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(file.filename)[1]
        file_path = os.path.join(settings.STORAGE_PATH, f"{file_id}{file_extension}")
        
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Create contract entity
        contract = ContractEntity(
            file_name=file.filename,
            business_owner=business_owner or "Unknown",
            department=department or "Unknown",
            file_path=file_path,
            extracted_text="[Pending analysis]"
        )
        db.add(contract)
        db.commit()
        db.refresh(contract)
        
        return contract
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{contract_id}", response_model=ContractModel)
async def get_contract(contract_id: str, db: Session = Depends(get_db)):
    """Get contract by ID"""
    contract = db.query(ContractEntity).filter(
        ContractEntity.contract_id == contract_id
    ).first()
    
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    return contract

@router.get("/", response_model=List[ContractSummary])
async def list_contracts(db: Session = Depends(get_db)):
    """List all contracts"""
    contracts = db.query(ContractEntity).order_by(ContractEntity.created_at.desc()).all()
    return contracts

@router.get("/{contract_id}/findings", response_model=List[RiskFindingModel])
async def get_findings(contract_id: str, db: Session = Depends(get_db)):
    """Get findings for a contract"""
    findings = db.query(RiskFindingEntity).filter(
        RiskFindingEntity.contract_id == contract_id
    ).all()
    return findings

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import os

from ..db import get_db
from ..models.contracts import ContractEntity, ContractModel, ContractSummary, RiskLevel
from ..models.findings import RiskFindingEntity, RiskFindingModel
from ..config import settings
from ..services.analyzer import analyze, _LEVEL_ORDER
from ..services.policy import compare_to_policy, gap_summary
from ..utils.parser import extract_text, is_allowed

router = APIRouter(prefix="/api/contracts", tags=["contracts"])


@router.post("/upload", response_model=ContractModel)
async def upload_contract(
    file: UploadFile = File(...),
    business_owner: Optional[str] = Form(None),
    department: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Upload contract for analysis with auto risk assessment"""
    print(f"DEBUG: owner={business_owner}, dept={department}")
    try:
        if not is_allowed(file.filename):
            raise HTTPException(status_code=400, detail="Unsupported file type")

        os.makedirs(settings.storage_path, exist_ok=True)
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(file.filename)[1]
        file_path = os.path.join(settings.storage_path, f"{file_id}{file_extension}")

        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        text = extract_text(file.filename, contents)
        if not text.strip():
            raise HTTPException(status_code=400, detail="No readable text found")

        result = analyze(text)
        gaps = compare_to_policy(text)
        gs = gap_summary(gaps)

        highest_risk = result.overall_level
        if result.findings:
            highest_risk = max(result.findings, key=lambda f: _LEVEL_ORDER[f.level]).level

        contract = ContractEntity(
            file_name=file.filename,
            business_owner=business_owner or "Unknown",
            department=department or "Unknown",
            file_path=file_path,
            extracted_text=text[:5000],
            highest_risk_level=highest_risk,
            summary=f"Analyzed: {len(result.findings)} risks. Compliance: {gs['compliance_pct']}%. Score: {result.score}/100"
        )
        db.add(contract)
        db.commit()
        db.refresh(contract)

        for finding in result.findings:
            risk_finding = RiskFindingEntity(
                contract_id=contract.contract_id,
                clause_reference=finding.keyword,
                description=finding.description,
                level=finding.level.value,
                recommendation=finding.recommendation,
                evidence=finding.snippet
            )
            db.add(risk_finding)

        db.commit()
        return contract
    except HTTPException:
        raise
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

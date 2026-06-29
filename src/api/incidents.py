from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..db import get_db
from ..models.incidents import IncidentEntity, IncidentModel, IncidentCreate

router = APIRouter(prefix="/api/incidents", tags=["incidents"])

@router.post("", response_model=IncidentModel)
async def create_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db)
):
    """Create a new incident"""
    db_incident = IncidentEntity(**incident.dict())
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

@router.get("/{incident_id}", response_model=IncidentModel)
async def get_incident(incident_id: str, db: Session = Depends(get_db)):
    """Get incident by ID"""
    incident = db.query(IncidentEntity).filter(
        IncidentEntity.incident_id == incident_id
    ).first()
    
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    return incident

@router.get("", response_model=List[IncidentModel])
async def list_incidents(db: Session = Depends(get_db)):
    """List all incidents"""
    incidents = db.query(IncidentEntity).order_by(
        IncidentEntity.date.desc()
    ).all()
    return incidents

@router.put("/{incident_id}", response_model=IncidentModel)
async def update_incident(
    incident_id: str,
    incident: IncidentCreate,
    db: Session = Depends(get_db)
):
    """Update incident"""
    db_incident = db.query(IncidentEntity).filter(
        IncidentEntity.incident_id == incident_id
    ).first()
    
    if not db_incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    for key, value in incident.dict().items():
        setattr(db_incident, key, value)
    
    db.commit()
    db.refresh(db_incident)
    return db_incident

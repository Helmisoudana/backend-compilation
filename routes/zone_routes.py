from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database.db import get_db
from models.zone import Zone
from schemas.schemas import ZoneCreate, ZoneUpdate, ZoneOut

router = APIRouter(prefix="/zones", tags=["Zones"])


# ── CREATE ────────────────────────────────────────────────────────────────────
@router.post("/", response_model=ZoneOut, status_code=status.HTTP_201_CREATED,
             summary="Créer une zone")
def create_zone(payload: ZoneCreate, db: Session = Depends(get_db)):
    zone = Zone(**payload.model_dump())
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone


# ── READ ALL ──────────────────────────────────────────────────────────────────
@router.get("/", response_model=List[ZoneOut], summary="Lister toutes les zones")
def get_zones( db: Session = Depends(get_db),):
    q = db.query(Zone)
    return q


# ── READ ONE ──────────────────────────────────────────────────────────────────
@router.get("/{id_zone}", response_model=ZoneOut, summary="Obtenir une zone par ID")
def get_zone(id_zone: int, db: Session = Depends(get_db)):
    zone = db.query(Zone).filter(Zone.id_zone == id_zone).first()
    if not zone:
        raise HTTPException(status_code=404, detail=f"Zone {id_zone} introuvable")
    return zone


# ── UPDATE ────────────────────────────────────────────────────────────────────
@router.put("/{id_zone}", response_model=ZoneOut, summary="Mettre à jour une zone")
def update_zone(id_zone: int, payload: ZoneUpdate, db: Session = Depends(get_db)):
    zone = db.query(Zone).filter(Zone.id_zone == id_zone).first()
    if not zone:
        raise HTTPException(status_code=404, detail=f"Zone {id_zone} introuvable")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(zone, field, value)
    db.commit()
    db.refresh(zone)
    return zone


# ── DELETE ────────────────────────────────────────────────────────────────────
@router.delete("/{id_zone}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Supprimer une zone")
def delete_zone(id_zone: int, db: Session = Depends(get_db)):
    zone = db.query(Zone).filter(Zone.id_zone == id_zone).first()
    if not zone:
        raise HTTPException(status_code=404, detail=f"Zone {id_zone} introuvable")
    db.delete(zone)
    db.commit()

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.evenement import Evenement
from app.schemas.evenement import EvenementCreate, EvenementUpdate, EvenementResponse

router = APIRouter(prefix="/evenements", tags=["🗓️ Événements"])


@router.get("/", response_model=List[EvenementResponse], summary="Lister tous les événements")
def get_evenements(
    statut: Optional[str] = Query(None, description="Filtrer par statut"),
    categorie: Optional[str] = Query(None, description="Filtrer par catégorie"),
    db: Session = Depends(get_db)
):
    query = db.query(Evenement)
    if statut:
        query = query.filter(Evenement.statut == statut)
    if categorie:
        query = query.filter(Evenement.categorie_activite == categorie)
    return query.order_by(Evenement.date_prevue.desc()).all()


@router.get("/stats", summary="Statistiques des événements")
def get_stats_evenements(db: Session = Depends(get_db)):
    from sqlalchemy import func
    total = db.query(func.count(Evenement.id_evenement)).scalar() or 0
    par_statut = db.query(Evenement.statut, func.count(Evenement.id_evenement)).group_by(Evenement.statut).all()
    return {
        "total": total,
        "par_statut": {s: c for s, c in par_statut if s}
    }


@router.get("/{id_evenement}", response_model=EvenementResponse)
def get_evenement(id_evenement: int, db: Session = Depends(get_db)):
    ev = db.query(Evenement).filter(Evenement.id_evenement == id_evenement).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Événement introuvable")
    return ev


@router.post("/", response_model=EvenementResponse, status_code=status.HTTP_201_CREATED, summary="Créer un événement")
def create_evenement(data: EvenementCreate, db: Session = Depends(get_db)):
    ev = Evenement(**data.model_dump())
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev


@router.put("/{id_evenement}", response_model=EvenementResponse, summary="Modifier un événement")
def update_evenement(id_evenement: int, data: EvenementUpdate, db: Session = Depends(get_db)):
    ev = db.query(Evenement).filter(Evenement.id_evenement == id_evenement).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Événement introuvable")
    for key, value in data.model_dump().items():
        setattr(ev, key, value)
    db.commit()
    db.refresh(ev)
    return ev


@router.delete("/{id_evenement}", status_code=status.HTTP_204_NO_CONTENT)
def delete_evenement(id_evenement: int, db: Session = Depends(get_db)):
    ev = db.query(Evenement).filter(Evenement.id_evenement == id_evenement).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Événement introuvable")
    db.delete(ev)
    db.commit()

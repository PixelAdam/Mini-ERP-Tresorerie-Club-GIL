from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.membre import Membre
from app.schemas.membre import MembreCreate, MembreUpdate, MembreResponse

router = APIRouter(prefix="/membres", tags=["👥 Membres"])


@router.get("/", response_model=List[MembreResponse], summary="Lister tous les membres")
def get_membres(
    search: Optional[str] = Query(None, description="Recherche par nom ou prénom"),
    cellule: Optional[str] = Query(None, description="Filtrer par cellule"),
    db: Session = Depends(get_db)
):
    query = db.query(Membre)
    if search:
        query = query.filter(
            (Membre.nom.ilike(f"%{search}%")) | (Membre.prenom.ilike(f"%{search}%"))
        )
    if cellule:
        query = query.filter(Membre.cellule == cellule)
    return query.all()


@router.get("/{id_membre}", response_model=MembreResponse, summary="Détails d'un membre")
def get_membre(id_membre: int, db: Session = Depends(get_db)):
    membre = db.query(Membre).filter(Membre.id_membre == id_membre).first()
    if not membre:
        raise HTTPException(status_code=404, detail="Membre introuvable")
    return membre


@router.post("/", response_model=MembreResponse, status_code=status.HTTP_201_CREATED, summary="Ajouter un membre")
def create_membre(data: MembreCreate, db: Session = Depends(get_db)):
    membre = Membre(**data.model_dump())
    db.add(membre)
    db.commit()
    db.refresh(membre)
    return membre


@router.put("/{id_membre}", response_model=MembreResponse, summary="Modifier un membre")
def update_membre(id_membre: int, data: MembreUpdate, db: Session = Depends(get_db)):
    membre = db.query(Membre).filter(Membre.id_membre == id_membre).first()
    if not membre:
        raise HTTPException(status_code=404, detail="Membre introuvable")
    for key, value in data.model_dump().items():
        setattr(membre, key, value)
    db.commit()
    db.refresh(membre)
    return membre


@router.delete("/{id_membre}", status_code=status.HTTP_204_NO_CONTENT, summary="Supprimer un membre")
def delete_membre(id_membre: int, db: Session = Depends(get_db)):
    membre = db.query(Membre).filter(Membre.id_membre == id_membre).first()
    if not membre:
        raise HTTPException(status_code=404, detail="Membre introuvable")
    db.delete(membre)
    db.commit()

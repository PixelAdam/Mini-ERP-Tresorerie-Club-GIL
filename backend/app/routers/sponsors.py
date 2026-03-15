from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from decimal import Decimal
from app.database import get_db
from app.models.sponsor import Sponsor
from app.models.sponsorisation import Sponsorisation
from app.models.evenement import Evenement
from app.schemas.sponsor import SponsorCreate, SponsorUpdate, SponsorResponse, SponsorisationCreate, SponsorisationResponse

router = APIRouter(prefix="/sponsors", tags=["🤝 Sponsors"])


@router.get("/", response_model=List[SponsorResponse], summary="Lister tous les sponsors")
def get_sponsors(
    statut: Optional[str] = Query(None, description="Filtrer par statut (Confirmé / En négociation)"),
    db: Session = Depends(get_db)
):
    query = db.query(Sponsor)
    if statut:
        query = query.filter(Sponsor.statut == statut)
    return query.all()


@router.get("/stats", summary="Statistiques des sponsors")
def get_stats_sponsors(db: Session = Depends(get_db)):
    total_confirmes = db.query(func.sum(Sponsor.montant_accorde)).filter(Sponsor.statut == "Confirmé").scalar() or Decimal("0")
    nb_confirmes = db.query(func.count(Sponsor.id_sponsor)).filter(Sponsor.statut == "Confirmé").scalar() or 0
    nb_negociation = db.query(func.count(Sponsor.id_sponsor)).filter(Sponsor.statut == "En négociation").scalar() or 0
    return {
        "montant_total_confirme": total_confirmes,
        "nb_confirmes": nb_confirmes,
        "nb_en_negociation": nb_negociation,
        "total": nb_confirmes + nb_negociation
    }


@router.get("/{id_sponsor}", response_model=SponsorResponse)
def get_sponsor(id_sponsor: int, db: Session = Depends(get_db)):
    sponsor = db.query(Sponsor).filter(Sponsor.id_sponsor == id_sponsor).first()
    if not sponsor:
        raise HTTPException(status_code=404, detail="Sponsor introuvable")
    return sponsor


@router.post("/", response_model=SponsorResponse, status_code=status.HTTP_201_CREATED, summary="Ajouter un sponsor")
def create_sponsor(data: SponsorCreate, db: Session = Depends(get_db)):
    sponsor = Sponsor(**data.model_dump())
    db.add(sponsor)
    db.commit()
    db.refresh(sponsor)
    return sponsor


@router.put("/{id_sponsor}", response_model=SponsorResponse, summary="Modifier un sponsor")
def update_sponsor(id_sponsor: int, data: SponsorUpdate, db: Session = Depends(get_db)):
    sponsor = db.query(Sponsor).filter(Sponsor.id_sponsor == id_sponsor).first()
    if not sponsor:
        raise HTTPException(status_code=404, detail="Sponsor introuvable")
    for key, value in data.model_dump().items():
        setattr(sponsor, key, value)
    db.commit()
    db.refresh(sponsor)
    return sponsor


@router.delete("/{id_sponsor}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sponsor(id_sponsor: int, db: Session = Depends(get_db)):
    sponsor = db.query(Sponsor).filter(Sponsor.id_sponsor == id_sponsor).first()
    if not sponsor:
        raise HTTPException(status_code=404, detail="Sponsor introuvable")
    db.delete(sponsor)
    db.commit()


# ── Sponsorisations (liaison Sponsor ↔ Événement) ──────────────────────────

@router.get("/{id_sponsor}/evenements", summary="Événements liés à un sponsor")
def get_evenements_sponsor(id_sponsor: int, db: Session = Depends(get_db)):
    sponsor = db.query(Sponsor).filter(Sponsor.id_sponsor == id_sponsor).first()
    if not sponsor:
        raise HTTPException(status_code=404, detail="Sponsor introuvable")
    liens = db.query(Sponsorisation).filter(Sponsorisation.id_sponsor == id_sponsor).all()
    ids_ev = [l.id_evenement for l in liens]
    evenements = db.query(Evenement).filter(Evenement.id_evenement.in_(ids_ev)).all()
    return evenements


@router.post("/sponsorisations", response_model=SponsorisationResponse, status_code=status.HTTP_201_CREATED, summary="Lier un sponsor à un événement")
def create_sponsorisation(data: SponsorisationCreate, db: Session = Depends(get_db)):
    # Vérifier l'existence des deux entités
    if not db.query(Sponsor).filter(Sponsor.id_sponsor == data.id_sponsor).first():
        raise HTTPException(status_code=404, detail="Sponsor introuvable")
    if not db.query(Evenement).filter(Evenement.id_evenement == data.id_evenement).first():
        raise HTTPException(status_code=404, detail="Événement introuvable")
    # Vérifier doublon
    existing = db.query(Sponsorisation).filter(
        Sponsorisation.id_sponsor == data.id_sponsor,
        Sponsorisation.id_evenement == data.id_evenement
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Ce sponsor est déjà lié à cet événement")
    lien = Sponsorisation(**data.model_dump())
    db.add(lien)
    db.commit()
    db.refresh(lien)
    return lien


@router.delete("/sponsorisations/{id_sponsor}/{id_evenement}", status_code=status.HTTP_204_NO_CONTENT, summary="Supprimer un lien sponsor-événement")
def delete_sponsorisation(id_sponsor: int, id_evenement: int, db: Session = Depends(get_db)):
    lien = db.query(Sponsorisation).filter(
        Sponsorisation.id_sponsor == id_sponsor,
        Sponsorisation.id_evenement == id_evenement
    ).first()
    if not lien:
        raise HTTPException(status_code=404, detail="Lien introuvable")
    db.delete(lien)
    db.commit()

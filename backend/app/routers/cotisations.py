from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional
from decimal import Decimal
from app.database import get_db
from app.models.cotisation import Cotisation
from app.models.membre import Membre
from app.schemas.cotisation import CotisationCreate, CotisationUpdate, CotisationResponse

router = APIRouter(prefix="/cotisations", tags=["💰 Cotisations"])


def _enrich(cot: Cotisation) -> dict:
    """Ajoute les infos du membre à la cotisation."""
    data = {c.name: getattr(cot, c.name) for c in cot.__table__.columns}
    data["membre_nom"] = cot.membre.nom if cot.membre else None
    data["membre_prenom"] = cot.membre.prenom if cot.membre else None
    return data


@router.get("/", response_model=List[CotisationResponse], summary="Lister toutes les cotisations")
def get_cotisations(
    id_membre: Optional[int] = Query(None, description="Filtrer par membre"),
    db: Session = Depends(get_db)
):
    query = db.query(Cotisation).options(joinedload(Cotisation.membre))
    if id_membre:
        query = query.filter(Cotisation.id_membre == id_membre)
    cotisations = query.all()
    return [_enrich(c) for c in cotisations]


@router.get("/stats", summary="Statistiques des cotisations")
def get_stats_cotisations(db: Session = Depends(get_db)):
    total = db.query(func.sum(Cotisation.montant)).scalar() or Decimal("0")
    nb_membres_actifs = db.query(func.count(func.distinct(Cotisation.id_membre))).scalar() or 0
    total_membres = db.query(func.count(Membre.id_membre)).scalar() or 0
    return {
        "total_cotisations": total,
        "nb_membres_ayant_paye": nb_membres_actifs,
        "total_membres": total_membres,
        "taux_paiement": round(nb_membres_actifs / total_membres * 100, 1) if total_membres else 0
    }


@router.get("/{id_cotisation}", response_model=CotisationResponse)
def get_cotisation(id_cotisation: int, db: Session = Depends(get_db)):
    cot = db.query(Cotisation).options(joinedload(Cotisation.membre)).filter(Cotisation.id_cotisation == id_cotisation).first()
    if not cot:
        raise HTTPException(status_code=404, detail="Cotisation introuvable")
    return _enrich(cot)


@router.post("/", response_model=CotisationResponse, status_code=status.HTTP_201_CREATED, summary="Enregistrer un paiement")
def create_cotisation(data: CotisationCreate, db: Session = Depends(get_db)):
    # Vérifier que le membre existe
    membre = db.query(Membre).filter(Membre.id_membre == data.id_membre).first()
    if not membre:
        raise HTTPException(status_code=404, detail="Membre introuvable")
    cot = Cotisation(**data.model_dump())
    db.add(cot)
    db.commit()
    db.refresh(cot)
    # Recharger avec relation
    cot = db.query(Cotisation).options(joinedload(Cotisation.membre)).filter(Cotisation.id_cotisation == cot.id_cotisation).first()
    return _enrich(cot)


@router.put("/{id_cotisation}", response_model=CotisationResponse)
def update_cotisation(id_cotisation: int, data: CotisationUpdate, db: Session = Depends(get_db)):
    cot = db.query(Cotisation).filter(Cotisation.id_cotisation == id_cotisation).first()
    if not cot:
        raise HTTPException(status_code=404, detail="Cotisation introuvable")
    for key, value in data.model_dump().items():
        setattr(cot, key, value)
    db.commit()
    db.refresh(cot)
    cot = db.query(Cotisation).options(joinedload(Cotisation.membre)).filter(Cotisation.id_cotisation == cot.id_cotisation).first()
    return _enrich(cot)


@router.delete("/{id_cotisation}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cotisation(id_cotisation: int, db: Session = Depends(get_db)):
    cot = db.query(Cotisation).filter(Cotisation.id_cotisation == id_cotisation).first()
    if not cot:
        raise HTTPException(status_code=404, detail="Cotisation introuvable")
    db.delete(cot)
    db.commit()

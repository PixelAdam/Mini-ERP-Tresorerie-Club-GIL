from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Optional
from decimal import Decimal
from datetime import date
from app.database import get_db
from app.models.transaction import TransactionClub, TransactionType
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse, TresorerieStats

router = APIRouter(prefix="/transactions", tags=["📊 Transactions"])


@router.get("/", response_model=List[TransactionResponse], summary="Lister toutes les transactions")
def get_transactions(
    type: Optional[TransactionType] = Query(None, description="Filtrer par type (income / expense)"),
    date_debut: Optional[date] = Query(None, description="Date de début (YYYY-MM-DD)"),
    date_fin: Optional[date] = Query(None, description="Date de fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    query = db.query(TransactionClub)
    if type:
        query = query.filter(TransactionClub.type == type)
    if date_debut:
        query = query.filter(TransactionClub.date_transaction >= date_debut)
    if date_fin:
        query = query.filter(TransactionClub.date_transaction <= date_fin)
    return query.order_by(TransactionClub.date_transaction.desc()).all()


@router.get("/stats", response_model=TresorerieStats, summary="Solde et statistiques de trésorerie")
def get_stats_tresorerie(db: Session = Depends(get_db)):
    revenus = db.query(func.sum(TransactionClub.montant)).filter(TransactionClub.type == TransactionType.income).scalar() or Decimal("0")
    depenses = db.query(func.sum(TransactionClub.montant)).filter(TransactionClub.type == TransactionType.expense).scalar() or Decimal("0")
    nb = db.query(func.count(TransactionClub.id_transaction)).scalar() or 0
    return TresorerieStats(
        total_revenus=revenus,
        total_depenses=depenses,
        solde=revenus - depenses,
        nb_transactions=nb
    )


@router.get("/stats/mensuel", summary="Évolution mensuelle des transactions")
def get_stats_mensuel(
    annee: Optional[int] = Query(None, description="Filtrer par année (ex: 2025)"),
    db: Session = Depends(get_db)
):
    query = db.query(
        extract("year", TransactionClub.date_transaction).label("annee"),
        extract("month", TransactionClub.date_transaction).label("mois"),
        TransactionClub.type,
        func.sum(TransactionClub.montant).label("total")
    )
    if annee:
        query = query.filter(extract("year", TransactionClub.date_transaction) == annee)
    rows = query.group_by("annee", "mois", TransactionClub.type).order_by("annee", "mois").all()

    result = {}
    for row in rows:
        key = f"{int(row.annee)}-{int(row.mois):02d}"
        if key not in result:
            result[key] = {"mois": key, "revenus": 0, "depenses": 0}
        if row.type == TransactionType.income:
            result[key]["revenus"] = float(row.total)
        else:
            result[key]["depenses"] = float(row.total)

    return list(result.values())


@router.get("/{id_transaction}", response_model=TransactionResponse)
def get_transaction(id_transaction: int, db: Session = Depends(get_db)):
    t = db.query(TransactionClub).filter(TransactionClub.id_transaction == id_transaction).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transaction introuvable")
    return t


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED, summary="Enregistrer une transaction")
def create_transaction(data: TransactionCreate, db: Session = Depends(get_db)):
    t = TransactionClub(**data.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


@router.put("/{id_transaction}", response_model=TransactionResponse, summary="Modifier une transaction")
def update_transaction(id_transaction: int, data: TransactionUpdate, db: Session = Depends(get_db)):
    t = db.query(TransactionClub).filter(TransactionClub.id_transaction == id_transaction).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transaction introuvable")
    for key, value in data.model_dump().items():
        setattr(t, key, value)
    db.commit()
    db.refresh(t)
    return t


@router.delete("/{id_transaction}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(id_transaction: int, db: Session = Depends(get_db)):
    t = db.query(TransactionClub).filter(TransactionClub.id_transaction == id_transaction).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transaction introuvable")
    db.delete(t)
    db.commit()

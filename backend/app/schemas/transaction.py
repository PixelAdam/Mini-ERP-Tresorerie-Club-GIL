from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import date
from app.models.transaction import TransactionType


class TransactionBase(BaseModel):
    date_transaction: date
    montant: Decimal = Field(..., gt=0)
    type: TransactionType
    description: Optional[str] = Field(None, max_length=255)


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id_transaction: int

    model_config = {"from_attributes": True}


# Schéma pour le dashboard trésorerie
class TresorerieStats(BaseModel):
    total_revenus: Decimal
    total_depenses: Decimal
    solde: Decimal
    nb_transactions: int

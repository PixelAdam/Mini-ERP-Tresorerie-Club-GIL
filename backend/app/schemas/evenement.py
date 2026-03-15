from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import date


class EvenementBase(BaseModel):
    nom: str = Field(..., max_length=150)
    date_prevue: date
    lieu: Optional[str] = Field(None, max_length=50)
    statut: Optional[str] = Field(None, max_length=20)
    categorie_activite: Optional[str] = Field(None, max_length=50)
    budget_activite: Optional[Decimal] = Field(None, ge=0)


class EvenementCreate(EvenementBase):
    pass


class EvenementUpdate(EvenementBase):
    pass


class EvenementResponse(EvenementBase):
    id_evenement: int

    model_config = {"from_attributes": True}

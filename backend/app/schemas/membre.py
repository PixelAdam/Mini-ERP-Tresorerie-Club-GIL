from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class MembreBase(BaseModel):
    nom: str = Field(..., max_length=100, examples=["Benali"])
    prenom: str = Field(..., max_length=100, examples=["Yassine"])
    niveau_etude: Optional[str] = Field(None, max_length=50, examples=["2ème année"])
    cellule: Optional[str] = Field(None, max_length=100, examples=["Trésorerie"])
    montant_cotisation: Decimal = Field(default=Decimal("0.00"), ge=0)


class MembreCreate(MembreBase):
    pass


class MembreUpdate(MembreBase):
    pass


class MembreResponse(MembreBase):
    id_membre: int

    model_config = {"from_attributes": True}

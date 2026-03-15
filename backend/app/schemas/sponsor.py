from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class SponsorBase(BaseModel):
    nom_entreprise: str = Field(..., max_length=150)
    nom_responsable: Optional[str] = Field(None, max_length=50)
    responsable_contact: Optional[str] = Field(None, max_length=150)
    montant_accorde: Optional[Decimal] = Field(None, ge=0)
    statut: Optional[str] = Field(None, max_length=50)


class SponsorCreate(SponsorBase):
    pass


class SponsorUpdate(SponsorBase):
    pass


class SponsorResponse(SponsorBase):
    id_sponsor: int

    model_config = {"from_attributes": True}


# Schéma pour lier un sponsor à un événement
class SponsorisationCreate(BaseModel):
    id_sponsor: int
    id_evenement: int


class SponsorisationResponse(SponsorisationCreate):
    model_config = {"from_attributes": True}

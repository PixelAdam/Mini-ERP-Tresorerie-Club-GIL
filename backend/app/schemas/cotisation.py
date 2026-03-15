from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import date


class CotisationBase(BaseModel):
    id_membre: int
    date_paiement: date
    montant: Decimal = Field(..., gt=0)


class CotisationCreate(CotisationBase):
    pass


class CotisationUpdate(CotisationBase):
    pass


class CotisationResponse(CotisationBase):
    id_cotisation: int
    # Infos du membre incluses dans la réponse
    membre_nom: Optional[str] = None
    membre_prenom: Optional[str] = None

    model_config = {"from_attributes": True}

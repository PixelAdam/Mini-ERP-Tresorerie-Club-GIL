from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from app.database import Base


class Sponsor(Base):
    __tablename__ = "sponsor"

    id_sponsor = Column(Integer, primary_key=True, autoincrement=True)
    nom_entreprise = Column(String(150), nullable=False)
    nom_responsable = Column(String(50), nullable=True)
    responsable_contact = Column(String(150), nullable=True)
    montant_accorde = Column(Numeric(10, 2), nullable=True)
    statut = Column(String(50), nullable=True)

    sponsorisations = relationship("Sponsorisation", back_populates="sponsor", cascade="all, delete")

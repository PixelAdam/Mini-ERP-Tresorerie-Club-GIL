from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from app.database import Base


class Membre(Base):
    __tablename__ = "membre"

    id_membre = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    niveau_etude = Column(String(50), nullable=True)
    cellule = Column(String(100), nullable=True)
    montant_cotisation = Column(Numeric(10, 2), nullable=False, default=0.00)

    cotisations = relationship("Cotisation", back_populates="membre", cascade="all, delete")

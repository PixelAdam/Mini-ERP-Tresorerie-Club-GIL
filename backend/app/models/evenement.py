from sqlalchemy import Column, Integer, String, Numeric, Date
from sqlalchemy.orm import relationship
from app.database import Base


class Evenement(Base):
    __tablename__ = "evenement"

    id_evenement = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(150), nullable=False)
    date_prevue = Column(Date, nullable=False)
    lieu = Column(String(50), nullable=True)
    statut = Column(String(20), nullable=True)
    categorie_activite = Column(String(50), nullable=True)
    budget_activite = Column(Numeric(10, 2), nullable=True)

    sponsorisations = relationship("Sponsorisation", back_populates="evenement", cascade="all, delete")

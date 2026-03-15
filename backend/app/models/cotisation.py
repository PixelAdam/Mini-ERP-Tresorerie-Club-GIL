from sqlalchemy import Column, Integer, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Cotisation(Base):
    __tablename__ = "cotisation"

    id_cotisation = Column(Integer, primary_key=True, autoincrement=True)
    id_membre = Column(Integer, ForeignKey("membre.id_membre", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    date_paiement = Column(Date, nullable=False)
    montant = Column(Numeric(10, 2), nullable=False)

    membre = relationship("Membre", back_populates="cotisations")

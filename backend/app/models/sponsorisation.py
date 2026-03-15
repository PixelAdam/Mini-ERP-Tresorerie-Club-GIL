from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Sponsorisation(Base):
    __tablename__ = "sponsorisation"

    id_sponsor = Column(Integer, ForeignKey("sponsor.id_sponsor", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    id_evenement = Column(Integer, ForeignKey("evenement.id_evenement", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

    sponsor = relationship("Sponsor", back_populates="sponsorisations")
    evenement = relationship("Evenement", back_populates="sponsorisations")

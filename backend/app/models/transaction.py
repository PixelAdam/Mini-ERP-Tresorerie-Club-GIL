from sqlalchemy import Column, Integer, Numeric, Date, String, Enum
from app.database import Base
import enum


class TransactionType(str, enum.Enum):
    income = "income"
    expense = "expense"


class TransactionClub(Base):
    __tablename__ = "transaction_club"

    id_transaction = Column(Integer, primary_key=True, autoincrement=True)
    date_transaction = Column(Date, nullable=False)
    montant = Column(Numeric(10, 2), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    description = Column(String(255), nullable=True)

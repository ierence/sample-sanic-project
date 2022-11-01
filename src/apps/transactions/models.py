from db.base_class import BaseModel
from sqlalchemy import Column, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from utils.mixins import NumericalIdMixin


class Transaction(NumericalIdMixin, BaseModel):
    __tablename__ = "transactions"

    balance_id = Column(UUID(as_uuid=True), ForeignKey("balances.id"))
    balance = relationship("Balance", back_populates="transactions")
    change = (Column(Float(precision=2)))

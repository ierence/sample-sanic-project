from db.base_class import BaseModel
from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from utils.mixins import NumericalIdMixin


class Balance(NumericalIdMixin, BaseModel):
    __tablename__ = "balances"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="balances")
    balance = (Column(Float(precision=2)))
    transactions = relationship("Transaction", back_populates='balance')

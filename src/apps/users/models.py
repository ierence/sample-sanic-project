from db.base_class import BaseModel
from sqlalchemy import Boolean, Column, String, LargeBinary
from sqlalchemy.orm import relationship
from utils.mixins import NumericalIdMixin


class User(NumericalIdMixin, BaseModel):
    __tablename__ = "users"

    username = Column(String(), unique=True)
    hashed_password = Column(LargeBinary())
    salt = Column(LargeBinary())
    activated = Column(Boolean(), default=False)
    active = Column(Boolean(), default=True)

    scope_records = relationship('ScopeRecord', back_populates='user')
    balances = relationship('Balance', back_populates='user')
    activation_link = relationship(
        'ActivationLink', back_populates='user', uselist=False)

from uuid import uuid4

from db.base_class import BaseModel
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class ScopeRecord(BaseModel):
    __tablename__ = "scope_records"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="scope_records")
    value = Column(String())


class ActivationLink(BaseModel):
    __tablename__ = "activation_links"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    user = relationship("User", back_populates="activation_link")
    link = Column(UUID(as_uuid=True), default=uuid4)

from db.base_class import BaseModel
from sqlalchemy import Column, Float, String


class Product(BaseModel):
    __tablename__ = 'products'

    title = Column(String())
    description = Column(String())
    price = Column(Float(precision=2))

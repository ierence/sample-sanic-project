from random import randint

from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class NumericalIdMixin(object):
    numerical_id = Column(Integer, default=randint(1, 100000000), unique=True)

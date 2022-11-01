from typing import List

from apps.balances.schemas import BalanceRetrieve, BalanceRetrieveOpenapi
from pydantic import BaseModel, types


class UserCreate(BaseModel):
    username: str
    password: str


class ScopeRecord(BaseModel):
    id: types.UUID4
    value: str

    class Config:
        orm_mode = True


class ScopeRecordOpenapi(ScopeRecord):
    id: str


class UserRetrieve(BaseModel):
    id: types.UUID4
    username: str
    activated: bool
    active: bool
    scope_records: List[ScopeRecord]
    balances: List[BalanceRetrieve]

    class Config:
        orm_mode = True


class UserRetrieveOpenapi(UserRetrieve):
    id: str
    scope_records: List[ScopeRecordOpenapi]
    balances: List[BalanceRetrieveOpenapi]


class UserUpdate(BaseModel):
    username: str
    activated: bool
    active: bool


class UserRegistration(BaseModel):
    id: types.UUID4
    username: str
    activation_link: str


class UserRegistrationOpenapi(UserRegistration):
    id: str

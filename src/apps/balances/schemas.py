from typing import List, Union
from uuid import UUID
from pydantic import BaseModel, types


class Transaction(BaseModel):
    id: types.UUID4
    change: float
    
    class Config:
        orm_mode = True

class TransactionOpenapi(Transaction):
    id:str

class BalanceRetrieve(BaseModel):
    id: types.UUID4
    balance: float
    transactions: List[Transaction]
    
    class Config:
        orm_mode = True
        
class BalanceRetrieveOpenapi(BalanceRetrieve):
    id:str
    transactions: List[TransactionOpenapi]


class BalanceCreate(BaseModel):
    user_id: types.UUID4
    balance: float


class BalanceCreateOpenapi(BalanceCreate):
    user_id: str

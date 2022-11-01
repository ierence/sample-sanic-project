from pydantic import BaseModel, types


class TransactionRetrieve(BaseModel):
    id: types.UUID4
    change: float
    balance_id: types.UUID4

    class Config:
        orm_mode = True


class TransactionRetrieveOpenapi(TransactionRetrieve):
    id: str
    balance_id: str

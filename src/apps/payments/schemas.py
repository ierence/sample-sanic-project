from pydantic import BaseModel, validator
from utils.webhook_signature import generate_signature


class Webhook(BaseModel):
    signature: str
    transaction_id: int
    user_id: int
    bill_id: int
    amount: int

    @validator('amount')
    def price_not_negative(cls, value):
        if value < 0:
            raise ValueError("цена должна быть больше 0")
        else:
            return value

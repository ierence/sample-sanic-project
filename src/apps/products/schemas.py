from pydantic import BaseModel, types, validator


class ProductRetrieve(BaseModel):
    id: types.UUID4
    title: str
    description: str
    price: float

    class Config:
        orm_mode = True


class ProductRetrieveOpenapi(ProductRetrieve):
    id: str


class ProductUpdate(BaseModel):
    title: str
    description: str
    price: float

    @validator('price')
    def price_not_negative(cls, value):
        if value < 0:
            raise ValueError("цена должна быть больше 0")
        else:
            return value

    class Config:
        orm_mode = True


class ProductCreate(BaseModel):
    title: str
    description: str
    price: float

    @validator('price')
    def price_not_negative(cls, value):
        if value < 0:
            raise ValueError("цена должна быть больше 0")
        else:
            return value

    class Config:
        orm_mode = True


class Order(BaseModel):
    balance_id: types.UUID4
    product_id: types.UUID4


class OrderOpenapi(Order):
    balance_id: str
    product_id: str

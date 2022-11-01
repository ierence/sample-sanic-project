from pydantic import BaseModel


class AuthRequestSchema(BaseModel):
    username: str
    password: str


class AuthResponseSchema(BaseModel):
    access_token: str

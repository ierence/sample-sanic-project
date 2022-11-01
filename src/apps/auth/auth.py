from typing import List

import jwt
from sanic.blueprints import Blueprint
from sanic.request import Request
from sanic.response import json
from sanic_ext import openapi
from sanic_httpauth import HTTPTokenAuth
from utils.uuid_encder import UUIDEncoder

from .schemas import AuthRequestSchema
from .services import authenticate

auth = HTTPTokenAuth("Bearer")
bp = Blueprint('auth', url_prefix="auth")


class AuthData():
    def __init__(self):
        pass

    def extract_data(self, request, auth):
        auth_data = decode_token(request, auth)
        self.scopes = auth_data["scopes"]
        self.user_id = auth_data["user_id"]
        self.active = auth_data["active"]
        self.activated = auth_data["activated"]

    def scopes_requiered(self, request, auth, scopes: List[str] = []):
        self.extract_data(request, auth)

        if all(scope in self.scopes for scope in scopes):
            return True

        return False

    def is_active(self, request, auth):
        self.extract_data(request, auth)

        return all([self.activated, self.active])


auth_data = AuthData()


async def generate_token(request: Request):
    auth_data = await authenticate(request=request)

    token = jwt.encode(
        auth_data, 'SUPER SECRET', "HS256", json_encoder=UUIDEncoder
    )

    return token


def decode_token(request, auth):
    verified_data = auth.token(request)

    auth_data = jwt.decode(
        verified_data, "SUPER SECRET", ["HS256"]
    )

    return auth_data


auth = HTTPTokenAuth("Bearer")
auth_data = AuthData()
bp = Blueprint('auth', url_prefix="auth")


@auth.verify_token
def verify_token(token):
    try:
        return "user_id", 'scopes', 'active', 'activated' in jwt.decode(
            token, "SUPER SECRET", ["HS256"]
        )
    except:
        return False


@bp.post('/')
@openapi.summary("Аунтефикация пользователя")
@openapi.body(AuthRequestSchema)
@openapi.response(200, str)
async def authenticate_user(request):
    token = await generate_token(request=request)

    return json(token, status=200)

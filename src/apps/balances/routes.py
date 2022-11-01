from apps.auth.auth import auth, auth_data
from sanic.response import json, text
from sanic.views import HTTPMethodView
from sanic_ext import openapi, validate

from .schemas import (
    BalanceCreate, 
    BalanceRetrieve,
    BalanceRetrieveOpenapi, 
    BalanceCreateOpenapi
)
from .services import create_balance, create_balance_for_user


@openapi.secured("token")
@openapi.summary('Создаёт новый баланс для текущего пользователя')
@openapi.response(200, {'application/json': BalanceRetrieveOpenapi})
@auth.login_required
async def balance_for_user(request):
    # auth
    if not auth_data.is_active(request, auth):
        return text("Ваш аккаунт деактивирован", 401)

    # create new balance
    balance = await create_balance_for_user(request, auth_data.user_id)

    # construct responce
    balance = BalanceRetrieve.from_orm(balance).dict()

    return json(balance, 200)


class BalancesView(HTTPMethodView):
    @openapi.secured('token')
    @openapi.summary('Создаёт новый баланс')
    @openapi.body({"application/json": BalanceCreateOpenapi})
    @openapi.response(200, {'application/json': BalanceRetrieveOpenapi})
    @validate(BalanceCreate)
    @auth.login_required
    async def post(self, request, body: BalanceCreate):
        # auth
        if not auth_data.scopes_requiered(request, auth, ['user', 'admin']):
            return text("Требуется авторизация", status=401)
        if not auth_data.active:
            return text("Ваш аккаунт деактивирован", 401)

        # create new balance
        balance = await create_balance(request, body)

        # construct responce
        balance = BalanceRetrieve.from_orm(balance).dict()

        return json(balance, 200)

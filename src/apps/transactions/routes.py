from apps.auth.auth import auth, auth_data
from sanic.response import json, text
from sanic.views import HTTPMethodView
from sanic_ext import openapi

from .schemas import TransactionRetrieve, TransactionRetrieveOpenapi
from .selectors import list_transactions


class TransactionsView(HTTPMethodView):
    @openapi.secured("token")
    @openapi.summary("Возвращает список всех транзакций")
    @openapi.response(200, {"application/json": TransactionRetrieveOpenapi})
    @auth.login_required
    async def get(self, request):
        # auth
        if not auth_data.scopes_requiered(request, auth, ['user', 'admin']):
            return text("Требуется авторизация", status=401)
        if not auth_data.active:
            return text("Ваш аккаунт деактивирован", 401)

        # query transactions
        transactions = await list_transactions(request)

        # construct responce
        transactions = [TransactionRetrieve.from_orm(
            transaction).dict() for transaction in transactions]

        return json(transactions, 200)

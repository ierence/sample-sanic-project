from apps.transactions.schemas import TransactionRetrieveOpenapi, TransactionRetrieve
from sanic.response import json
from sanic_ext import openapi, validate

from .schemas import Webhook
from .services import process_webhook


@openapi.summary("Эндпоинт для зачисления баланса с помощью стороннего сервиса")
@openapi.body({'application/json': Webhook})
@openapi.response(200, {"application/json": TransactionRetrieveOpenapi})
@validate(Webhook)
async def webhook(request, body: Webhook):
    # precess webhook
    transaction = await process_webhook(request, body)
    # construct responce
    transaction = TransactionRetrieve.from_orm(transaction).dict()
    return json(transaction, 200)

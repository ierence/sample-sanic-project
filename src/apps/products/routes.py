from apps.auth.auth import auth, auth_data
from apps.balances.schemas import BalanceRetrieve
from sanic.response import json, text
from sanic.views import HTTPMethodView
from sanic_ext import openapi, validate

from .schemas import Order, ProductCreate, ProductRetrieve, ProductUpdate, ProductRetrieveOpenapi, OrderOpenapi
from .selectors import list_product
from .services import (create_product, destroy_product, process_order,
                       update_product)


@openapi.secured("token")
@openapi.summary('Списывает со счета, принадлежащего пользователю, стоимость продукта')
@openapi.body({'application/json': OrderOpenapi})
@openapi.response(200, {'application/json': ProductRetrieveOpenapi})
@validate(Order)
@auth.login_required
async def buy(request, body: Order):
    if not auth_data.is_active(request, auth):
        return text("Ваш аккаунт деактивирован", 401)

    # process order
    balance = await process_order(request, body, auth_data)

    # construct response
    balance = BalanceRetrieve.from_orm(balance).dict()

    return json(balance, 200)


class ProductsView(HTTPMethodView):
    # List
    @openapi.secured("token")
    @openapi.summary("Возвращает список всех продуктов")
    @openapi.response(200, {'application/json': [ProductRetrieveOpenapi]})
    @auth.login_required
    async def get(self, request):
        # Query products
        products = await list_product(request)

        # Consctuct response
        products = [
            ProductRetrieve.from_orm(product).dict() for product in products
        ]
        res = json(products, status=200)

        return res

    # Create
    @openapi.secured("token")
    @openapi.summary("Создает новый продукт")
    @openapi.body({"application/json": ProductCreate})
    @openapi.response(200, {'application/json': ProductRetrieveOpenapi})
    @validate(ProductCreate)
    @auth.login_required
    async def post(self, request, body: ProductCreate):
        # auth
        if not auth_data.scopes_requiered(request, auth, ['user', 'admin']):
            return text("Требуется авторизация", status=401)
        if not auth_data.active:
            return text("Ваш аккаунт деактивирован", 401)
        # Create new product
        product = await create_product(request, body)
        # Construct response
        product = ProductRetrieve.from_orm(product).dict()
        res = json(product, 200)
        return res


class ProductView(HTTPMethodView):
    # update
    @openapi.secured('token')
    @openapi.summary('Обновляет продукт')
    @openapi.body({"application/json": ProductUpdate})
    @openapi.response(200, {"application/json": ProductRetrieveOpenapi})
    @validate(ProductUpdate)
    @auth.login_required
    async def put(self, request, body, pk):
        # auth
        if not auth_data.scopes_requiered(request, auth, ['user', 'admin']):
            return text("Требуется авторизация", status=401)
        if not auth_data.active:
            return text("Ваш аккаунт деактивирован", 401)

        # Update product
        product = await update_product(request, body, pk)

        # Construct Response
        product = ProductRetrieve.from_orm(product).dict()
        res = json(product, status=200)

        return res

    # destroy
    @openapi.secured("token")
    @openapi.summary("Удаляет продукт")
    @openapi.response(200, {"application/json": ProductRetrieveOpenapi})
    @auth.login_required
    async def delete(self, request, pk):
        # auth
        if not auth_data.scopes_requiered(request, auth, ['user', 'admin']):
            return text("Требуется авторизация", status=401)
        if not auth_data.active:
            return text("Ваш аккаунт деактивирован", 401)

        # Update product
        product = await destroy_product(request, pk)

        # Construct Response
        product = ProductRetrieve.from_orm(product).dict()
        res = json(product, status=200)

        return res

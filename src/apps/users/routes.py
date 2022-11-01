from urllib.request import Request

from apps.auth.auth import auth, auth_data
from sanic.request import Request
from sanic.response import json, text
from sanic.views import HTTPMethodView
from sanic_ext import openapi, validate

from .schemas import (
    UserCreate,
    UserRegistration,
    UserRetrieve,
    UserUpdate,
    UserRegistrationOpenapi,
    UserRetrieveOpenapi
)
from .selectors import list_users, retrieve_user
from .services import activate_user, create_user, update_user


class ActivateView(HTTPMethodView):
    @openapi.summary("Активирует пользователя с помощью ссылки активации")
    async def get(self, request: Request, key):
        # Activate user
        await activate_user(request, key)

        return text("Пользователь активирован.")


class UsersView(HTTPMethodView):
    @openapi.summary("Создаёт нового пользователя")
    @openapi.body({"application/json": UserCreate})
    @openapi.response(200, {"application/json": UserRegistrationOpenapi})
    @validate(UserCreate)
    async def post(self, request: Request, body):
        # Register user
        user = await create_user(request, body)

        # Construct Responce
        activation_link = request.host + "/users/activate/" + \
            str(user.activation_link.link)
        user = user.__dict__
        user['activation_link'] = activation_link
        user = UserRegistration(**user).dict()
        res = json(user, status=200)

        return res

    @openapi.secured("token")
    @openapi.summary("Возвращает список всех пользователей")
    @openapi.response(200, {'application/json': [UserRetrieveOpenapi]})
    @auth.login_required
    async def get(self, request):
        # Auth
        if not auth_data.scopes_requiered(request, auth, ['user', 'admin']):
            return text("Недостаточо прав", status=401)
        if not auth_data.is_active(request, auth):
            return text("Ваш аккаунт деактивирован", 401)

        # Query users
        users = await list_users(request)

        # Construct Responce
        users = [UserRetrieve.from_orm(user).dict() for user in users]
        res = json(users, status=200)

        return res


class UserView(HTTPMethodView):
    @openapi.secured("token")
    @openapi.summary('Возращает данные о конкретном пользователе')
    @openapi.response(200, {"application/json": UserRetrieveOpenapi})
    @auth.login_required
    async def get(self, request, pk):
        # Auth
        if not auth_data.scopes_requiered(request, auth, ['user', 'admin']):
            return text("Недостаточо прав", status=401)
        if not auth_data.is_active(request, auth):
            return text("Ваш аккаунт деактивирован", 401)

        # Query user
        user = await retrieve_user(request, pk)

        # Construct Response
        user = UserRetrieve.from_orm(user).dict()
        res = json(user, status=200)

        return res

    @openapi.secured("token")
    @openapi.summary("Обновляет данные о пользователе")
    @openapi.body({'application/json': UserUpdate})
    @openapi.response(200, {'application/json': UserRetrieveOpenapi})
    @auth.login_required
    async def put(self, request, pk):
        # Auth
        if not auth_data.scopes_requiered(request, auth, ['user', 'admin']):
            return text("Недостаточо прав", status=401)
        if not auth_data.is_active(request, auth):
            return text("Ваш аккаунт деактивирован", 401)

        # Update user
        user = await update_user(request, pk)

        # Construct Response
        user = UserRetrieve.from_orm(user).dict()
        res = json(user, status=200)

        return res


@openapi.secured("token")
@openapi.summary("Возвращает данные о текущем пользователе")
@openapi.response(200, {"application/json": UserRetrieveOpenapi})
@auth.login_required
async def me(request):
    # auth
    if not auth_data.is_active(request, auth):
        return text("Ваш аккаунт деактивирован", 401)

    # retrieve user
    user = await retrieve_user(request, auth_data.user_id)

    # construct response    
    user = UserRetrieve.from_orm(user).dict()

    res = json(user, status=200)

    return res

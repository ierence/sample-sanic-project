from sanic import Blueprint

from .routes import ActivateView, UsersView, UserView, me

bp = Blueprint("users", url_prefix="users")

bp.add_route(UsersView.as_view(), '/', methods=['POST', 'GET'])
bp.add_route(UserView.as_view(), '/<pk:str>', methods=['GET', 'PUT'])
bp.add_route(ActivateView.as_view(), '/activate/<key:str>')
bp.add_route(me, '/me')

from sanic.blueprints import Blueprint

from .routes import BalancesView, balance_for_user

bp = Blueprint('balances', url_prefix='balances')

bp.add_route(BalancesView.as_view(), '/')
bp.add_route(balance_for_user, '/for_me', ['POST'])

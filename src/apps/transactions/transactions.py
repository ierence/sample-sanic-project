from sanic import Blueprint

from .routes import TransactionsView

bp = Blueprint("transactions", url_prefix="transactions")

bp.add_route(TransactionsView.as_view(), '/')

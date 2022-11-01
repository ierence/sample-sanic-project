from sanic.blueprints import Blueprint

from .routes import webhook

bp = Blueprint('payments', 'payment')

bp.add_route(webhook, 'webhook', ["POST"])

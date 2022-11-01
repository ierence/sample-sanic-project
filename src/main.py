from sanic import Sanic
from db.bind import _base_model_session_ctx, _sessionmaker

from apps.auth.auth import bp as auth_bp
from apps.balances.balances import bp as balances_bp
from apps.payments.payments import bp as payments_bp
from apps.products.products import bp as products_bp
from apps.transactions.transactions import bp as transactions_bp
from apps.users.users import bp as users_bp
from configuration import CONFIG

from utils.uuid_encder import uuid_dumps

app = Sanic(__name__, dumps=uuid_dumps)
app.update_config(CONFIG)
app.blueprint([users_bp,
               auth_bp,
               products_bp,
               balances_bp,
               transactions_bp,
               payments_bp])

app.ext.openapi.add_security_scheme(
    "token",
    "http",
    scheme="bearer",
    bearer_format="JWT",
)


@app.middleware("request")
async def inject_session(request):
    request.ctx.session = _sessionmaker()
    request.ctx.session_ctx_token = _base_model_session_ctx.set(
        request.ctx.session)


@app.middleware("response")
async def close_session(request, response):
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()


if __name__ == "__main__":
    app.run(
        dev=CONFIG['DEV']
    )

from apps.balances.models import Balance
from apps.balances.selectors import retrieve_balance_by_numerical_id
from apps.transactions.models import Transaction
from apps.users.selectors import retrieve_user_by_numerical_id
from utils.webhook_signature import generate_signature

from .schemas import Webhook


async def process_webhook(request, body: Webhook):
    # verify secret key
    signature = generate_signature(
        body.transaction_id,
        body.user_id,
        body.bill_id,
        body.amount
    )

    assert signature == body.signature

    # retrieve or create balance, then modify it
    balance: Balance = await retrieve_balance_by_numerical_id(request, body.bill_id)

    if not balance:
        user = await retrieve_user_by_numerical_id(request, body.user_id)

        balance = Balance(
            numerical_id=body.bill_id,
            user=user,
            balance=0
        )

    balance.balance += body.amount  # type: ignore
    # create transaction

    transaction = Transaction(
        numerical_id=body.transaction_id,
        balance=balance,
        change=body.amount
    )

    request.ctx.session.add(transaction)
    await request.ctx.session.commit()

    return transaction

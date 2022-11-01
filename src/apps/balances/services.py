from apps.users.selectors import retrieve_user

from .models import Balance
from .schemas import BalanceCreate, Transaction


async def create_balance(request, body: BalanceCreate):

    user = await retrieve_user(request, body.user_id)

    balance = Balance(
        balance=body.balance,
        user=user
    )

    request.ctx.session.add(balance)

    await request.ctx.session.commit()

    return balance


async def create_balance_for_user(request, pk):

    user = await retrieve_user(request, pk)

    balance = Balance(
        balance=0,
        user=user,
        transactions=[]
    )

    request.ctx.session.add(balance)

    await request.ctx.session.commit()

    return balance

from sqlalchemy import select

from .models import Balance


async def retrieve_balance(request, pk):
    stmt = select(Balance).where(Balance.id == pk)
    
    result = await request.ctx.session.scalars(stmt)
    
    balance: Balance = result.first()
    return balance


async def retrieve_balance_by_numerical_id(request, pk):
    stmt = select(Balance).where(Balance.numerical_id == pk)
    
    result = await request.ctx.session.scalars(stmt)
    
    balance: Balance = result.first()
    return balance


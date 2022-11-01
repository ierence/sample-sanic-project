from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .models import User

from apps.balances.models import Balance


async def list_users(request):
    stmt = select(User).options(
        selectinload(User.scope_records),
        selectinload(User.balances).selectinload(Balance.transactions)
    )
    result = await request.ctx.session.scalars(stmt)
    
    users = result.all()
    
    return users


async def retrieve_user(request, pk):
    stmt = select(User).where(User.id == pk).options(
        selectinload(User.scope_records),
        selectinload(User.balances).selectinload(Balance.transactions)
        
    )
    result = await request.ctx.session.scalars(stmt)
    
    user: User = result.first()
    return user


async def retrieve_user_by_numerical_id(request, pk):
    stmt = select(User).where(User.numerical_id == pk).options(
        selectinload(User.scope_records),
        selectinload(User.balances),
    )
    result = await request.ctx.session.scalars(stmt)
    
    user: User = result.first()
    return user


from .models import Transaction
from sqlalchemy import select

from typing import List


async def list_transactions(request) -> List[Transaction]:
    stmt = select(Transaction)
    
    result = await request.ctx.session.scalars(stmt)
    
    transactions = result.all()
    
    return transactions
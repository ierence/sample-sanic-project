from .models import Product
from sqlalchemy import select


async def list_product(request):
    stmt = select(Product)
    result = await request.ctx.session.scalars(stmt)
    
    users = result.all()
    
    return users


async def retrieve_product(request, pk):
    stmt = select(Product).where(Product.id == pk)
    result = await request.ctx.session.scalars(stmt)
    
    user = result.first()
    
    return user

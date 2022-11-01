from shutil import ExecError
from .models import Product
from .schemas import ProductCreate, ProductUpdate, Order
from .selectors import retrieve_product

from apps.users.selectors import retrieve_user


async def create_product(request, body: ProductCreate):
    product_dict = body.dict()

    product = Product(
        **product_dict
    )
        
    request.ctx.session.add(product)

    await request.ctx.session.commit()
    
    return product


async def update_product(request, body: ProductUpdate, pk):
    
    product = await retrieve_product(request, pk)
    
    for key, value in body.__dict__.items():
        setattr(product, key, value)
    
    await request.ctx.session.commit()
    
    return product


async def destroy_product(request, pk):
    
    product = await retrieve_product(request, pk)
    
    await request.ctx.session.delete(product)
    
    await request.ctx.session.commit()
    
    return product


async def process_order(request, body: Order, auth_data):
    
    user = await retrieve_user(request, auth_data.user_id)
    
    balance = next(balance for balance in user.balances if balance.id == body.balance_id)
    
    product = await retrieve_product(request, body.product_id)
    
    if balance.balance >= product.price:
        balance.balance -= product.price 
    else:
        raise ExecError("На счёту недостаточно средств!")
    
    await request.ctx.session.commit()
    
    return balance
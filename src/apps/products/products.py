from sanic.blueprints import Blueprint

from .routes import ProductsView, ProductView, buy

bp = Blueprint('products', url_prefix='products')

bp.add_route(ProductsView.as_view(), '/')
bp.add_route(ProductView.as_view(), '/<pk:str>')
bp.add_route(buy, '/buy', ['POST'])

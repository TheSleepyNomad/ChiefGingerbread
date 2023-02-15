from sqlalchemy.exc import NoResultFound

from app.database.main import Database
from app.database.models import Products, Order
from app.utils.utils import _convert_in_UserCart

def get_all_products():
    session = Database().session
    result = session.query(Products).all()
    session.close()
    return result

def get_product_by_id(id:int):
    session = Database().session
    result = session.query(Products).filter(Products.id == id).one()
    session.close()
    return result

def get_count_all_products():
    session = Database().session
    result = session.query(Products).count()
    session.close()
    return result

def get_cart_by_user(user_telegram_id: int):
    session = Database().session
    user_cart = session.query(Order.id, Order.quantity, Products.name, Products.price)\
        .filter(Order.user_telegram_id == user_telegram_id)\
            .filter(Order.product_id == Products.id).all()
    cart = _convert_in_UserCart(user_cart)
    session.close()
    return cart

def get_selected_cart_item(user_telegram_id: int, order_id: int):
    session = Database().session
    user_cart = session.query(Order.id, Order.quantity, Products.name, Products.price).filter(Order.id == order_id and Order.user_telegram_id == user_telegram_id)\
        .filter(Products.id == Order.product_id).all()
    cart = _convert_in_UserCart(user_cart)
    session.close()
    return cart
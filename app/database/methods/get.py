from sqlalchemy.exc import NoResultFound

from app.database.main import Database
from app.database.models import Products, Order


def get_all_products():
    session = Database().session
    result = session.query(Products).all()
    print(type(result))
    session.close()
    return result

def get_count_all_products():
    session = Database().session
    result = session.query(Products).count()
    print(type(result))
    print(result)
    session.close()
    return result

def get_cart_by_user(user_telegram_id: int):
    session = Database().session
    cart = session.query(Order.quantity, Order.product_id).filter(Order.user_telegram_id == user_telegram_id).all()
    user_cart = session.query(Order.quantity, Products.name, Products.price).filter(Order.user_telegram_id == user_telegram_id).filter(Order.product_id == Products.id).all()
    print(user_cart)
    session.close()
    return cart
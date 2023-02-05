from sqlalchemy.exc import NoResultFound

from app.database.main import Database
from app.database.models import Products, Order

def create_order_record(product_id: int, user_telegram_id: int) -> None:
        session = Database().session
        session.add(Order(quantity=1,product_id=product_id,user_telegram_id=user_telegram_id))
        session.commit()


def update_order_record(product_id: int, user_telegram_id: int) -> None:
     session = Database().session
     session.query(Order).filter(Order.id == product_id and Order.user_telegram_id == user_telegram_id).update({'quantity': Order.quantity + 1})
     session.commit()

def check_order_exist(product_id: int, user_telegram_id: int) -> bool:
    session = Database().session
    try:
        session.query(Order).filter(Order.product_id == product_id and Order.user_telegram_id == user_telegram_id).one()
        session.close()
        return True
    except NoResultFound:
        session.close()
        return False
from sqlalchemy.exc import NoResultFound

from app.database.main import Database
from app.database.models import Products, Order

def reduce_order_record(product_id: int, user_telegram_id: int) -> None:
        session = Database().session
        try:
            product_in_cart = session.query(Order.id).filter(Order.product_id == product_id).one()
            product_in_cart.update({'quantity': Order.quantity - 1})
            session.commit()
        except NoResultFound:
            session.add(Order(quantity=1,product_id=product_id,user_telegram_id=user_telegram_id))
            session.commit()
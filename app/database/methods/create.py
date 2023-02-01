from sqlalchemy.exc import NoResultFound

from app.database.main import Database
from app.database.models import Products, Order

def create_order_record(product_id: int, user_telegram_id: int) -> None:
        #! dublicate quantity!!!!
        #! dont forget fix this
        session = Database().session
        try:
            session.query(Order.id).filter(Order.product_id == product_id).one()
        except NoResultFound:
            session.add(Order(quantity=1,product_id=product_id,user_telegram_id=user_telegram_id))

        session.query(Order).filter(Order.product_id == product_id).update({'quantity': Order.quantity + 1})
        session.commit()

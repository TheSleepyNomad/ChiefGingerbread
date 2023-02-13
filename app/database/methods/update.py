from sqlalchemy.exc import NoResultFound

from app.database.main import Database
from app.database.models import Products, Order

def reduce_order_record(order_id: int) -> bool:
        session = Database().session
        order = session.query(Order).filter(Order.id == order_id).one()
        if order.quantity <= 1:
                return False
        else:
                session.query(Order).filter(Order.id == order_id).update({'quantity': Order.quantity - 1})
                session.commit()
                return True
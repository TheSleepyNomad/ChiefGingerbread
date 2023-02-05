from sqlalchemy.exc import NoResultFound

from app.database.main import Database
from app.database.models import Products, Order

def reduce_order_record(order_id: int) -> None:
        session = Database().session
        session.query(Order).filter(Order.id == order_id).update({'quantity': Order.quantity - 1})
        session.commit()
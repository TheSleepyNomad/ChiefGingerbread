from sqlalchemy.exc import NoResultFound
from app.database.main import Database
from app.database.models import Products, Order


def delele_user_cart(user_telegram_id: int) -> bool:
    session = Database().session
    session.query(Order).filter(Order.user_telegram_id == user_telegram_id).delete()
    session.commit()
    return True
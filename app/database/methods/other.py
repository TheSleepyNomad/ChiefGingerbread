from sqlalchemy.exc import NoResultFound

from app.database.main import Database
from app.database.models import Products, Order

def check_user_baket_exist(user_telegram_id: int) -> bool:
        session = Database().session
        cart = session.query(Order.id).filter_by(user_telegram_id=user_telegram_id).exists()
        session.close()
        return True if cart else False
        # try:
        #     cart = session.query(Order.id).filter_by(user_telegram_id=user_telegram_id).exists()
        #     session.close()
        #     return True
        # except NoResultFound:
        #     session.close()
        #     return False
        

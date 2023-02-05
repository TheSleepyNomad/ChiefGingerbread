from sqlalchemy.exc import NoResultFound

from app.database.main import Database
from app.database.models import Products, Order

def check_user_baket_exist(user_telegram_id: int) -> bool:
        session = Database().session
        a = session.query(Order).all()
        print(a)
        try:
            print(user_telegram_id)
            session.query(Order.id).filter(Order.user_telegram_id == user_telegram_id).one()
            session.close()
            return True
        except NoResultFound:
            session.close()
            return False
        

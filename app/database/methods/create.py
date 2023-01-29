from sqlalchemy.exc import NoResultFound

from app.database.main import Database
from app.database.models import Users


def create_user(telegram_id: int) -> None:
    session = Database().session
    try:
        session.query(Users.telegram_id).filter(Users.telegram_id == telegram_id).one()
    except NoResultFound:
        session.add(Users(telegram_id=telegram_id))
        session.commit()
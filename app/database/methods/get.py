from sqlalchemy.exc import NoResultFound

from app.database.main import Database
from app.database.models import Products


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
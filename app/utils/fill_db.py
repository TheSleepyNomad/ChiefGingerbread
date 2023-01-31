from sqlalchemy.exc import NoResultFound
from app.database.main import Database
from app.database.models import Order, Products


def fill_database() -> None:
    session = Database().session
    session.add(Products(name='Имя1',title='Описание1',price=10.2,quantity=13,is_active=True))
    session.add(Products(name='Имя2',title='Описание2',price=15.2,quantity=13,is_active=True))
    session.add(Products(name='Имя3',title='Описание3',price=7,quantity=13,is_active=True))
    session.add(Products(name='Имя4',title='Описание4',price=8,quantity=13,is_active=True))
    session.add(Products(name='Имя5',title='Описание5',price=32,quantity=13,is_active=True))
    session.add(Products(name='Имя6',title='Описание6',price=45,quantity=13,is_active=True))
    session.add(Products(name='Имя7',title='Описание7',price=2,quantity=13,is_active=True))
    session.add(Products(name='Имя8',title='Описание8',price=0,quantity=13,is_active=True))
    session.commit()
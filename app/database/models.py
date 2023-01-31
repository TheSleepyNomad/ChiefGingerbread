from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from app.database.main import Database


class Products(Database.BASE):

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    title = Column(String)
    price = Column(Float)
    quantity =  Column(Integer)
    is_active = Column(Boolean)

    
    def __repr__(self) -> str:
        return f'{self.name} {self.title} {self.price}'
    

class Order(Database.BASE):

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    quantity =  Column(Integer)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_telegram_id = Column(Integer)
    date = Column(DateTime)

    products = relationship(Products, backref=backref('orders', uselist=True))

    
    def __repr__(self) -> str:
        return f'{self.quantity} {self.data}'



def register_models():
    Database.BASE.metadata.create_all(Database().engine)
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from app.database.main import Database
from json import dumps as json_dumps


class Products(Database.BASE):

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    title = Column(String)
    price = Column(Float)
    quantity =  Column(Integer)
    img_path = Column(String)
    is_active = Column(Boolean)

    
    def __repr__(self) -> str:
        # json string
        return json_dumps({'id': self.id,
                           'name': self.name,
                           'title': self.title,
                           'price': self.price,
                           'img_path': self.img_path,
                           'quantity': self.quantity})
    

class Order(Database.BASE):

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    quantity =  Column(Integer)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_telegram_id = Column(Integer)
    date = Column(DateTime(timezone=True), server_default=func.now())

    products = relationship(Products, backref=backref('orders', uselist=True))

    
    def __repr__(self) -> str:
        # json string
        return json_dumps({'id': self.id,
                           'quantity': self.quantity,
                           'product_id': self.product_id,
                           'user_telegram_id': self.user_telegram_id})



def register_models():
    Database.BASE.metadata.create_all(Database().engine)
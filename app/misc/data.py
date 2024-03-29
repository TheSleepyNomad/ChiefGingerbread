from sqlalchemy.engine.row import Row
from typing import List
from dataclasses import dataclass
from aiogram.types import CallbackQuery
from json import loads as json_loads


@dataclass(frozen=True, slots=True)
class MsgTemplate:
    welcome_msg = ''
    text_enter_msg = ''
    catalog_msg = ''
    product_card_msg = """
    Наименование: <b><i>{name}</i></b>

    Описание: {title}

    Стоимость: <i>{price}</i> руб.
    """
    

@dataclass
class UserCart:
    id: int
    quantity: int
    name: str
    price: float
    img: str


@dataclass
class QueryData:
    page: int = 0
    count_page: int = 0
    slicer: int = 0
    product_id: int = 0
    order_id: int = 0
    user_id: int = 0
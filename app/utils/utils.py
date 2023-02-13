from sqlalchemy.engine.row import Row
from typing import List
from dataclasses import dataclass
from aiogram.types import CallbackQuery
from json import loads as json_loads


@dataclass
class UserCart:
    id: int
    quantity: int
    name: str
    price: float

@dataclass
class QueryData:
    page: int = 0
    count_page: int = 0
    slicer: int = 0
    product_id: int = 0
    order_id: int = 0
    user_id: int = 0



def _convert_in_UserCart(user_cart: List[Row] | Row) -> List[UserCart]:
    cart = []
    for item in user_cart:
        cart.append(UserCart(id=item[0],
                             quantity=item[1],
                             name=item[2],
                             price=item[3]))
    return cart

def _get_data_from_json(query: CallbackQuery) -> QueryData:
    request = query.data.split('_')
    json_string = json_loads(request[0])
    data = QueryData(
        page=int(json_string['PageNum']) if 'PageNum' in request[0] else 0,
        count_page=int(json_string['CountPage']) if 'CountPage' in request[0] else 0,
        slicer=5*int(json_string['PageNum']) if 'PageNum' in request[0] else 0,
        product_id=int(json_string['prodId']) if 'prodId' in request[0] else 0,
        order_id=int(json_string['orderId']) if 'orderId' in request[0] else 0,
        user_id=int(json_string['userId']) if 'userId' in request[0] else 0)
    return data
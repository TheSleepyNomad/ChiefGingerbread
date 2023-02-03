from sqlalchemy.engine.row import Row
from typing import List
from dataclasses import dataclass


@dataclass
class UserCart:
    id: int
    quantity: int
    name: str
    price: float


def _convert_in_UserCart(user_cart: List[Row]) -> List[UserCart]:
    cart = []
    for item in user_cart:
        cart.append(UserCart(id=item[0],
                             quantity=item[1],
                             name=item[2],
                             price=item[3]))
    return cart

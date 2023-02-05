from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from app.database.methods.get import get_count_all_products, get_cart_by_user
from app.database.methods.other import check_user_baket_exist
from math import ceil

def create_start_markup(user_id: int) -> InlineKeyboardMarkup:
    count_products = get_count_all_products()
    count = ceil(count_products / 5)
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton('На сайт', callback_data='web_site'))
    markup.add(InlineKeyboardButton('Процесс готовки', callback_data='description'))
    markup.add(InlineKeyboardButton('Каталог', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":\"1\",\"CountPage\":"+ str(count) +"}"))
    if check_user_baket_exist(user_id):
        user_products_count = ceil(len(get_cart_by_user(user_id)) / 5)
        markup.add(InlineKeyboardButton('Корзина', callback_data="{\"page\":\"cart\",\"act\":\"pagin\",\"PageNum\":\"1\",\"CountPage\":" + str(user_products_count) + "}"))

    return markup
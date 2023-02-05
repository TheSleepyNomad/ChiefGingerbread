from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputFile, CallbackQuery
from app.config.config import START_LOGO
from app.database.methods.get import get_all_products, get_count_all_products, get_cart_by_user
from app.database.methods.other import check_user_baket_exist
from math import ceil


# start msg
async def send_welcome_msg(msg: Message):
    count_products = get_count_all_products()
    count = ceil(count_products / 5)
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton('На сайт', callback_data='web_site'))
    markup.add(InlineKeyboardButton('Процесс готовки', callback_data='description'))
    markup.add(InlineKeyboardButton('Каталог', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":\"1\",\"CountPage\":"+ str(count) +"}"))
    if check_user_baket_exist(msg.chat.id):
        # think about get count method from db
        user_products_count = ceil(len(get_cart_by_user(msg.chat.id)) / 5)
        markup.add(InlineKeyboardButton('Корзина', callback_data="{\"page\":\"cart\",\"act\":\"pagin\",\"PageNum\":\"1\",\"CountPage\":" + str(user_products_count) + "}"))
        
    with open(START_LOGO, 'rb') as img:
        await msg.bot.send_photo(msg.chat.id, photo=InputFile(img), caption='Привет!', reply_markup=markup)


def register_command_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome_msg, commands=['start'])
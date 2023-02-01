from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputFile, CallbackQuery
from app.config.config import START_LOGO
from app.database.methods.get import get_all_products, get_count_all_products
from app.database.methods.other import check_user_baket_exist
from math import ceil


# btns()
BTN_WEB_SITE = InlineKeyboardButton('На сайт', callback_data='web_site')
BTN_DESCRIPTION = InlineKeyboardButton('Процесс готовки', callback_data='description')
BTN_CATALOG = InlineKeyboardButton('Каталог', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":\"s\",\"CountPage\":\"s\"}")
# keyboard
START_MENU = InlineKeyboardMarkup().add(BTN_WEB_SITE).add(BTN_DESCRIPTION).add(BTN_CATALOG)
START_MENU1 = InlineKeyboardMarkup().add(BTN_CATALOG)


# handlers
# start msg
async def send_welcome_msg(msg: Message):
    count_products = get_count_all_products()
    count = ceil(count_products / 5)
    print(count)
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton('На сайт', callback_data='web_site'))
    markup.add(InlineKeyboardButton('Процесс готовки', callback_data='description'))
    markup.add(InlineKeyboardButton('Каталог', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":\"1\",\"CountPage\":"+ str(count) +"}"))

    if check_user_baket_exist:
        markup.add(InlineKeyboardButton('Корзина', callback_data=' '))
        
    with open(START_LOGO, 'rb') as img:
        await msg.bot.send_photo(msg.chat.id, photo=InputFile(img), caption='Привет!', reply_markup=markup)


def register_command_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome_msg, commands=['start'])
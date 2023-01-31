from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputFile, CallbackQuery
from app.config.config import START_LOGO
from app.database.methods.get import get_all_products, get_count_all_products


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
    count = round(count_products / 5) + 1
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton('На сайт', callback_data='web_site'))
    markup.add(InlineKeyboardButton('Процесс готовки', callback_data='description'))
    markup.add(InlineKeyboardButton('Каталог', callback_data="{\"page\":\"catalog\",\"act\":\"pagin\",\"PageNum\":\"1\",\"CountPage\":"+ str(count) +"}"))
    with open(START_LOGO, 'rb') as img:
        await msg.bot.send_photo(msg.chat.id, photo=InputFile(img), caption='Привет!', reply_markup=markup)


def register_command_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome_msg, commands=['start'])
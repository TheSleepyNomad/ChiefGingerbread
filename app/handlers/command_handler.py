from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from app.database.methods.create import create_user
from app.config.config import START_LOGO



# btns
BTN_WEB_SITE = InlineKeyboardButton('На сайт', callback_data='web_site')
BTN_DESCRIPTION = InlineKeyboardButton('Процесс готовки', callback_data='description')
BTN_CATALOG = InlineKeyboardButton('Каталог', callback_data='catalog')

# keyboard
START_MENU = InlineKeyboardMarkup().add(BTN_WEB_SITE).add(BTN_DESCRIPTION).add(BTN_CATALOG)


# handlers
# start msg
async def send_welcome_msg(msg: Message):
    # add new customer in DB
    create_user(msg.from_user.id)
    with open(START_LOGO, 'rb') as img:
        await msg.bot.send_photo(msg.chat.id, photo=InputFile(img), caption='Привет!', reply_markup=START_MENU)

    

def register_command_handlers(dp: Dispatcher):
    print('я запустился')
    dp.register_message_handler(send_welcome_msg, commands=['start'])
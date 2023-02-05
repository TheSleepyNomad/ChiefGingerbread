from aiogram import Dispatcher
from aiogram.types import Message, InputFile
from app.config.config import START_LOGO
from app.markup.markup import create_start_markup


# start msg
async def send_welcome_msg(msg: Message):        
    with open(START_LOGO, 'rb') as img:
        await msg.bot.send_photo(msg.chat.id, photo=InputFile(img), caption='Привет!', reply_markup=create_start_markup(msg.chat.id))


def register_command_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome_msg, commands=['start'])
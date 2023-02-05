from aiogram import Dispatcher
from aiogram.types import Message


# if user write something wrong
async def send_answer_for_unknow_msg(msg: Message):
    await msg.bot.send_message(msg.chat.id, text=f'Извини, {msg.from_user.first_name}'
                           f', но я Вас не понимаю, напишите /start!')
    

def register_other_handlers(dp: Dispatcher):

    dp.register_message_handler(send_answer_for_unknow_msg, content_types=['text'], state=None)

    
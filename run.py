from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import NetworkError
from dataclass import ApiKeys
from database.models import register_models

# start bot
bot = Bot(token=ApiKeys.BOT_TOKEN)
dp = Dispatcher(bot)

register_models()

# btns
BTN_WEB_SITE = InlineKeyboardButton('На сайт', callback_data='web_site')
BTN_DESCRIPTION = InlineKeyboardButton('Процесс готовки', callback_data='description')
BTN_CATALOG = InlineKeyboardButton('Каталог', callback_data='catalog')

# keyboard
START_MENU = InlineKeyboardMarkup().add(BTN_WEB_SITE).add(BTN_DESCRIPTION).add(BTN_CATALOG)


# handlers
# start msg
@dp.message_handler(commands=['start'])
async def send_welcome_msg(message: Message):
    await bot.send_message(message.chat.id, text='Привет', reply_markup=START_MENU)


# if user write something wrong
@dp.message_handler(content_types=['text'], state=None)
async def send_answer_for_unknow_msg(message: Message):
    await bot.send_message(message.chat.id, text=f'Извини, {message.from_user.first_name}'
                           f', но я Вас не понимаю, напишите /start!')

    
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
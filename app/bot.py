from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import NetworkError
from app.misc.env import ApiKeys
from app.handlers.main_handler import register_all_handlers
from app.database.models import register_models
from app.utils.fill_db import fill_database
from app.config.config import DEBUG_MODE


def __on_start_up(dp: Dispatcher):
    register_all_handlers(dp)
    register_models()
    if DEBUG_MODE:
        fill_database()
    

# start bot
def start_app():
    bot = Bot(token=ApiKeys.BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot)
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up(dp))
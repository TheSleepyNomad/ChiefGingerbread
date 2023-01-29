from aiogram import Dispatcher
from app.handlers.other_handler import register_other_handlers
from app.handlers.command_handler import register_command_handlers


def register_all_handlers(dp: Dispatcher):
    handlers = [register_command_handlers, register_other_handlers]

    for handler in handlers:
        print(handler)
        handler(dp)
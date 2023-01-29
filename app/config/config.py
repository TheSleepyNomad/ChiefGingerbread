from pathlib import Path
from aiogram.types import InputFile


BASE_DIR = Path(__file__).resolve().parent.parent
START_LOGO = BASE_DIR.joinpath('img').joinpath('welcome_msg_logo.jpg')


from pathlib import Path
from aiogram.types import InputFile

# root dit
BASE_DIR = Path(__file__).resolve().parent.parent
# media dirs
START_LOGO = BASE_DIR.joinpath('img').joinpath('welcome_msg_logo.jpg')
PLACEHOLDERS_DIR = BASE_DIR.joinpath('img').joinpath('placeholders')
# logs dir
LOGS_DIR = BASE_DIR.joinpath('logs')
# templates dirs
DOC_TEMPLATES_DIR = BASE_DIR.joinpath('misc').joinpath('templates')


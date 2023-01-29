from abc import ABC
from dotenv import load_dotenv
from os import environ
from typing import Final

load_dotenv()

class ApiKeys(ABC):
    BOT_TOKEN: Final = environ.get('BOT_TOKEN')
    KKM_TOKEN: Final = environ.get('KKM_TOKEN')


from loguru import logger
from dotenv import load_dotenv

load_dotenv()

logger.add('bot_state.log', format="{time}--{level}--{message}")

logger.debug("Hell")
logger.info('All Good')
logger.error('Die!!!')
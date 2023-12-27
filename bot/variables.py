import logging
import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

PASSWORD = os.getenv('PASSWORD')

URL = os.getenv('URL')

USER_CURRENCY = "€"

logger = logging.getLogger(__name__)

logging.basicConfig(
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot.log', 'a')],
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=os.getenv('debug', 'INFO')
)

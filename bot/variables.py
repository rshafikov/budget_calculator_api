import logging
import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv('TOKEN')

PASSWORD = os.getenv('PASSWORD')

URL = os.getenv('URL')

USER_CURRENCY = "€"

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
#
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger.
# # add formatter to c

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='bot.log',
    filemode='a',
    level=logging.INFO
)

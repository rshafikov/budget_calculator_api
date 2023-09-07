import logging
import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv('TOKEN')

URL = os.getenv('URL')

USER_CURRENCY = "€"

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='bot.log',
    filemode='a',
    level=logging.INFO
)

# from test_bot import TestBot
from variables import TOKEN

from bot import MyBot

if __name__ == '__main__':
    bot = MyBot(TOKEN)
    bot.start_polling()

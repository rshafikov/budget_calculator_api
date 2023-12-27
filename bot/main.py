from bot import MyBot
# from test_bot import TestBot
from variables import TOKEN

if __name__ == '__main__':
    bot = MyBot(TOKEN)
    bot.start_polling()

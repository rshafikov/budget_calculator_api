from bot import MyBot
from variables import TOKEN


if __name__ == '__main__':
    bot = MyBot(TOKEN)
    bot.start_polling()

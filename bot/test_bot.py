import json

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater


class TestBot:

    def __init__(self, token):
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(
            MessageHandler(Filters.text, self.handle_message))

    def start_polling(self):
        self.updater.start_polling()

    def handle_message(self, update, context):
        context.bot.send_message(
            text=(self.convert(
                '''
                {
                    "period": "week",
                    "total_per_period": 124.30000000000001,
                    "summary": [
                        {
                            "category__category_name": "YT_food",
                            "total": 10.5
                        },
                        {
                            "category__category_name": "chevapi",
                            "total": 6.0
                        },
                        {
                            "category__category_name": "coffee",
                            "total": 164343.5
                        },
                        {
                            "category__category_name": "domestic",
                            "total": 2.5
                        },
                        {
                            "category__category_name": "fastfood",
                            "total": 2.0
                        },
                        {
                            "category__category_name": "grocery",
                            "total": 45.3
                        },
                        {
                            "category__category_name": "sport",
                            "total": 41.5
                        }
                    ]
                }''')),
            chat_id=update.effective_chat.id,
            parse_mode='HTML'
        )

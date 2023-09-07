from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram import ReplyKeyboardMarkup
from user import User
from variables import USER_CURRENCY
from buttons import TABLE_MAIN_MENU, CATEGORIES, TABLE_OF_CATEGORIES
from variables import logging

buttons_categories = ReplyKeyboardMarkup(
    TABLE_OF_CATEGORIES, resize_keyboard=True)

buttons_table = ReplyKeyboardMarkup(TABLE_MAIN_MENU, resize_keyboard=True)

buttons_ok = ReplyKeyboardMarkup([['ДА ✅', 'НАЗАД 🔙']], resize_keyboard=True)


class MyBot:
    user_dict = {}

    def __init__(self, token):
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(
            CommandHandler('start', self.start_message))
        self.dispatcher.add_handler(
            MessageHandler(Filters.text, self.handle_message))

    def start_polling(self):
        self.updater.start_polling()

    @classmethod
    def get_or_create_user(cls, chat_id, update):
        if not cls.user_dict.get(chat_id):
            user = User(update)
            user.get_auth()
            cls.user_dict.update({user.id: user})
            return user

        return cls.user_dict.get(chat_id)

    @staticmethod
    def return_correct_date(date_string):
        new_string = date_string.split('T')
        date = new_string[0]
        time = new_string[1].split('.')[0]
        return f'🗓{date} 🕰{time}'

    @staticmethod
    def make_table(records_list):
        table = [(
            '{0:<12} {1:>7} {2}\n'
            .format(
                CATEGORIES[record["category"] - 1],
                record["total"],
                USER_CURRENCY)
        ) for record in records_list]
        return table

    def start_message(self, update, context):
        chat_id = update.effective_chat.id
        user = self.get_or_create_user(chat_id, update)
        context.bot.send_message(
            chat_id=user.id,
            text=(
                'Привет, {}. Я буду следить за вашим семейным бюджетом. '
                'Указывай категорию расхода, вводи сумму, смотри итог.'
                .format(user.first_name)
            ),
            reply_markup=buttons_table
        )

    def handle_message(self, update, context):
        chat_id = update.effective_chat.id
        user = self.get_or_create_user(chat_id, update)
        user.last_message = update.message.text
        if user.last_message in ['Записать расход', 'НАЗАД 🔙']:
            user.last_category = None
            user.last_summ = None
            context.bot.send_message(
                chat_id=chat_id,
                text='Укажите категорию расхода, пожалуйста',
                reply_markup=buttons_categories
            )
            logging.info(f'{user.id}: {user.first_name} - {user.last_message}')

        elif user.last_message == 'Cписок расходов за месяц':
            user.get_records_list()
            data = user.request_records_list.json()
            if data:
                context.bot.send_message(
                    chat_id=chat_id,
                    text=('\n'.join([
                        f'Дата: {self.return_correct_date(record.get("created"))}\n'
                        f'Категория: {record.get("category")}\n'
                        f'Сумма: {record.get("amount")} '
                        f'{USER_CURRENCY}\n' for record in data
                    ])
                    )
                )
            else:
                context.bot.send_message(
                    chat_id=chat_id,
                    text='В этом месяце еще не было расходов, записать расход?',
                    reply_markup=buttons_table
                )
                logging.info(f'{user.id}: {user.first_name} - {user.last_message}')

        elif user.last_message == 'Показать итоговую сводку':
            user.get_total()
            data = user.request_total.json()
            summary_list = ''.join(self.make_table(data.get('summary')))
            total_per_day = data.get("current_day")
            if not total_per_day:
                total_per_day = 0
            context.bot.send_message(
                chat_id=chat_id,

                text=(
                    f'За все время: {data.get("total")} {USER_CURRENCY}\n'
                    f'Ваши расходы за месяц: '
                    f'{data.get("current_month")} {USER_CURRENCY}\n'
                    f'Ваши расходы за день: {total_per_day} {USER_CURRENCY}\n'
                    'Категория    |    Тотал    \n'
                    '--------------------------\n'
                    f'{summary_list}'
                ),
                reply_markup=buttons_table
            )
            logging.info(f'{user.id}: {user.first_name} - {user.last_message}')

        elif user.last_message in CATEGORIES[:15]:
            user.last_category = user.last_message
            context.bot.send_message(
                chat_id=chat_id,
                text='Укажите сумму:'
            )

        elif user.last_message == '⚙️Меню':
            context.bot.send_message(
                chat_id=chat_id,
                text='Выберете действие',
                reply_markup=buttons_table
            )

        elif user.last_message.isdigit():
            user.last_summ = user.last_message
            if user.last_category:
                context.bot.send_message(
                    chat_id=chat_id,
                    text=(
                        f'Вы указали: \n'
                        '------------\n'
                        f'Категория: {user.last_category}\n'
                        f'Cумма: {user.last_message} {USER_CURRENCY}\n\n'
                        'Если верно, нажмите "ДА ✅"'
                    ),
                    reply_markup=buttons_ok
                )
            else:
                context.bot.send_message(
                    chat_id=chat_id,
                    text='Укажите категорию расхода, пожалуйста',
                    reply_markup=buttons_categories
                )

        elif user.last_message == 'ДА ✅':
            if user.last_summ and user.last_category:
                user.make_record()
                context.bot.send_message(
                    chat_id=chat_id,
                    text=(
                        'Записаны данные: ✅\n'
                        f'Категория: {user.last_category}\n'
                        f'Сумма: {user.last_summ} {USER_CURRENCY}\n\n'
                        f'Ожидаю новую запись :)'),
                    reply_markup=buttons_table
                )
                user.last_category = None
                user.last_summ = None
            else:
                context.bot.send_message(
                    chat_id=chat_id,
                    text='Укажите сумму:'
                )

        else:
            context.bot.send_message(
                chat_id=chat_id,
                text='Я вас не понимаю, выберете категорию расхода',
                reply_markup=buttons_categories
            )
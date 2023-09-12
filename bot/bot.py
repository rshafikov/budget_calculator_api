from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram import ReplyKeyboardMarkup
from user_interface.user import User
from user_interface.utility import make_table
from variables import USER_CURRENCY
from buttons import (
    TABLE_MAIN_MENU, CATEGORIES, TABLE_OF_CATEGORIES,
    BUTTON_OK, BUTTON_TABLE, button_user_categories)
from variables import logging


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
            cls.user_dict.update({user.id: user})
            return user
        return cls.user_dict.get(chat_id)

    def start_message(self, update, context):
        user = self.initiate_user(update, context)
        context.bot.send_message(
            chat_id=user.id,
            text=(
                f'Привет, {user.first_name}.'
                'Я буду следить за вашим семейным бюджетом. '
                'Итак:'
                '---------------------------------------'
                '1. Указывай категорию расхода;'
                '2. Вводи сумму;'
                '3. Смотри итог;'
                '---------------------------------------'
                'Меня не просили, но я посоветую:'
                'Записывай расход сразу после покупки, потом будет сложно вспомнить куда ушли все деньги.'
                'Старайся придерживаться минимализма при создании своих категорий:'
                'кофе <- хороший пример нейминга'
                'Коффе☕️👍 <- нейминг не очень, не спрашивай почему'
            ),
            reply_markup=BUTTON_TABLE
        )

    def initiate_user(self, update, context):
        chat_id = update.effective_chat.id
        user = self.get_or_create_user(chat_id, update)
        user.last_message = update.message.text
        return user

    @staticmethod
    def user_record_list(user: User, update, context):
        data = user.request_get_records_list().json()
        if data:
            context.bot.send_message(
                chat_id=user.id,
                text=('\n'.join([
                    # f'Дата: {self.return_correct_date(record.get("created"))}\n'
                    f'Категория: {record.get("category")}\n'
                    f'Сумма: {record.get("amount")} '
                    f'{USER_CURRENCY}\n' for record in data
                ]))
            )

    @staticmethod
    def user_choose_record(user, context):
        user.last_category = None
        user.last_summ = None
        context.bot.send_message(
            chat_id=user.id,
            text='Укажите категорию расхода, пожалуйста',
            reply_markup=ReplyKeyboardMarkup(
                [user.categories],
                resize_keyboard=True
            )
        )

    @staticmethod
    def user_month_records(user: User, context):
        data = user.request_get_records_list().json()
        if data:
            context.bot.send_message(
                chat_id=user.id,
                text=('\n'.join([
                    # f'Дата: {self.return_correct_date(record.get("created"))}\n'
                    f'Категория: {record.get("category")}\n'
                    f'Сумма: {record.get("amount")} '
                    f'{USER_CURRENCY}\n' for record in data
                ]))
            )
        else:
            context.bot.send_message(
                chat_id=user.id,
                text='В этом месяце еще не было расходов, записать расход?',
                reply_markup=ReplyKeyboardMarkup(
                    [user.categories],
                    resize_keyboard=True
                )
            )

    @staticmethod
    def user_total_records(user: User, context):
        data = user.request_get_total().json()
        summary_list = ''.join(make_table(data.get('summary')))
        total_per_day = data.get('current_day')
        total_per_week = data.get('current_week')
        if not total_per_day:
            total_per_day = 0
        context.bot.send_message(
            chat_id=user.id,
            text=(
                f'За все время: {data.get("total")} {USER_CURRENCY}\n'
                f'Ваши расходы за месяц: '
                f'{data.get("current_month")} {USER_CURRENCY}\n'
                f'Ваши расходы за день: {total_per_day} {USER_CURRENCY}\n'
                'Категория    |    Тотал    \n'
                '--------------------------\n'
                f'{summary_list}'),
            reply_markup=BUTTON_TABLE
        )

    @staticmethod
    def user_create_category(
            user: User, category_name, action, context):
        user.request_category(category_name, action)
        context.bot.send_message(
            chat_id=user.id,
            text='Категория успешно создана',
            reply_markup=button_user_categories(user.categories)
        )

    def handle_message(self, update, context):
        user = self.initiate_user(update, context)
        user_categories = user.categories
        if user.last_message in ['Записать расход', 'НАЗАД 🔙']:
            self.user_choose_record(user, context)

        elif user.last_message == 'NEW CATEGORY':
            user.last_category = user.last_message
            context.bot.send_message(
                chat_id=user.id,
                text='Укажите название категории'
            )
        elif user.last_category == 'NEW CATEGORY':
            context.bot.send_message(
                chat_id=user.id,
                text=(
                    'Создание новой категории\n'
                    f'Категория: {user.last_message}\n'
                    'Если верно, нажмите "ДА ✅"'
                ),
                reply_markup=BUTTON_OK
            )
        elif user.last_message == 'Cписок расходов за месяц':
            self.user_month_records(user, context)

        elif user.last_message == 'Показать итоговую сводку':
            self.user_total_records(user, context)

        elif user.last_message in ('⚙️Меню', 'НАЗАД 🔙'):
            context.bot.send_message(
                chat_id=user.id,
                text='Выберете действие',
                reply_markup=BUTTON_TABLE
            )

        elif user.last_message in user_categories:
            user.last_category = user.last_message
            context.bot.send_message(
                chat_id=user.id,
                text='Укажите сумму:'
            )

        elif user.last_message.isdigit():
            user.last_summ = user.last_message
            if user.last_category:
                context.bot.send_message(
                    chat_id=user.id,
                    text=(
                        f'Категория: {user.last_category}\n'
                        f'Cумма: {user.last_message} {USER_CURRENCY}\n\n'
                        'Если верно, нажмите "ДА ✅"'
                    ),
                    reply_markup=BUTTON_OK
                )
            else:
                context.bot.send_message(
                    chat_id=user.id,
                    text='Укажите категорию расхода, пожалуйста',
                    reply_markup=button_user_categories(user_categories)
                )

        elif user.last_message == 'ДА ✅':
            if user.last_summ and user.last_category:
                user.request_make_record()
                context.bot.send_message(
                    chat_id=user.id,
                    text=(
                        'Записаны данные: ✅\n'
                        f'Категория: {user.last_category}\n'
                        f'Сумма: {user.last_summ} {USER_CURRENCY}\n\n'
                        f'Ожидаю новую запись :)'),
                    reply_markup=BUTTON_TABLE
                )
                user.last_category = None
                user.last_summ = None
            elif not user.last_summ and user.last_category:
                user.last_category = None
                if not user.last_message in user_categories:
                    self.user_create_category(
                        user, user.last_message, 'POST', context)
                else:
                    context.bot.send_message(
                        chat_id=user.id,
                        text='Данная категория уже есть!'
                    )
            else:
                context.bot.send_message(
                    chat_id=user.id,
                    text='Укажите сумму:'
                )

        else:
            context.bot.send_message(
                chat_id=user.id,
                text='Я вас не понимаю, выберете категорию расхода',
                reply_markup=button_user_categories(user_categories)
            )

        logging.info(f'{user.id}: {user.first_name} - {user.last_message}')

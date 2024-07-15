import json
import textwrap

from buttons import (BUTTON_CURRENCY, BUTTON_OK, BUTTON_REPORTS, BUTTON_TABLE,
                     button_user_categories)
from prettytable import ALL, PrettyTable
from telegram.error import NetworkError
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from user_interface.user import User
from user_interface.utility import (execute_time_wrapper, is_float,
                                    prettify_total)
from variables import logging

LOG = logging.getLogger(__name__)


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
        try:
            self.updater.start_polling()
        except NetworkError as err:
            LOG.warning('Unable to connect to telegram API: %s', err)

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
                f'Привет, {user.first_name}. '
                'Я буду следить за вашим семейным бюджетом. '
                'Итак:\n'
                '---------------------------------\n'
                '1. Указывай категорию расхода\n'
                '2. Вводи сумму\n'
                '3. Смотри итог\n'
                '---------------------------------\n'
                'Меня не просили, но я посоветую:\n'
                'Записывай расход сразу после покупки, '
                'потом будет сложно вспомнить куда ушли все деньги. '
                'Старайся придерживаться минимализма '
                'при создании своих категорий:\n'
                'кофе <- хороший пример нейминга\n'
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
    def user_choose_record(user, context):
        user.last_category = None
        user.last_summ = None
        context.bot.send_message(
            chat_id=user.id,
            text='Укажите категорию расхода, пожалуйста',
            reply_markup=button_user_categories(user.categories)
        )

    @staticmethod
    def user_record_list(user: User, context):
        data = user.request_get_records_list().json()
        if data:
            context.bot.send_message(
                chat_id=user.id,
                text=json.dumps(data, indent=2),
            )
        else:
            context.bot.send_message(
                chat_id=user.id,
                text='В этом месяце еще не было расходов, записать расход?',
                reply_markup=button_user_categories(user.categories)
            )

    @staticmethod
    def user_total_records(user: User, context, period='день', custom=None):
        period = {
            'месяц': 'month',
            'неделю': 'week',
            'день': 'day'
        }[period] if not custom else custom
        output = textwrap.dedent(
            """
            <pre>Нет записей за {period}</pre>
            """
        ).format(period=period)
        try:
            data = user.request_get_total(
                period=f'?period={period}').json()
            if data['summary']:
                output = prettify_total(data, user.currency)
        except Exception as err:
            output = f'period: {period!r}\n**error**:\n {err}'
        context.bot.send_message(
            chat_id=user.id,
            text=output,
            parse_mode='HTML',
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

    @execute_time_wrapper
    def handle_message(self, update, context):
        user = self.initiate_user(update, context)
        user_categories = [c.lower() for c in user.categories]
        if user.last_message in ['Записать расход', 'НАЗАД 🔙']:
            self.user_choose_record(user, context)

        elif user.last_message == 'NEW CATEGORY':
            user.last_category = user.last_message
            context.bot.send_message(
                chat_id=user.id,
                text='Укажите название категории'
            )
        elif user.last_category == 'NEW CATEGORY':
            user.last_category = user.last_message
            context.bot.send_message(
                chat_id=user.id,
                text=(
                    'Создание новой категории\n'
                    f'Категория: {user.last_message}\n'
                    'Если верно, нажмите "ДА ✅"'
                ),
                reply_markup=BUTTON_OK
            )
        elif user.last_message == 'Выбрать валюту':
            context.bot.send_message(
                chat_id=user.id,
                text=(
                    'Укажите используемую валюту:\n'
                ),
                reply_markup=BUTTON_CURRENCY
            )
        elif user.last_message in ('EUR', 'RUB', 'USD', 'USDT'):
            user.currency = user.last_message
            context.bot.send_message(
                chat_id=user.id,
                text=(
                    f'Выбранная валюта: {user.currency}\n'
                ),
                reply_markup=BUTTON_TABLE
            )
        elif user.last_message == 'Отчеты':
            context.bot.send_message(
                chat_id=user.id,
                text='Выберете отчет',
                reply_markup=BUTTON_REPORTS
            )
        elif any([
                'за месяц' in user.last_message,
                'за неделю' in user.last_message,
                'за день' in user.last_message]):
            self.user_total_records(
                user, context, user.last_message.split()[2])

        elif user.last_message == 'Показать список расходов':
            self.user_record_list(user, context)

        elif user.last_message in ('⚙️Меню', 'НАЗАД 🔙'):
            context.bot.send_message(
                chat_id=user.id,
                text='Выберете действие',
                reply_markup=BUTTON_TABLE
            )

        elif user.last_message.lower() in user_categories:
            user.last_category = user.last_message
            context.bot.send_message(
                chat_id=user.id,
                text='Укажите сумму:'
            )

        elif user.last_message.isdigit() or is_float(user.last_message):
            user.last_summ = user.last_message
            if user.last_category:
                text = f'<pre>'
                table = PrettyTable(
                    field_names=('CATEGORY', user.currency),
                    hrules=ALL,
                    align='l',
                )
                table._max_width = {"CATEGORY": 17, user.currency: 7}
                table.add_row([user.last_category, user.last_message])
                text += (
                    table.get_string()
                    + '</pre>\nЕсли запись верна, нажмите "ДА ✅"')

                context.bot.send_message(
                    chat_id=user.id,
                    text=text,
                    parse_mode='HTML',
                    reply_markup=BUTTON_OK
                )
            else:
                context.bot.send_message(
                    chat_id=user.id,
                    text='Укажите категорию расхода, пожалуйста',
                    reply_markup=button_user_categories(user_categories)
                )

        elif user.last_message in ('ДА ✅', 'Yes', 'yes', 'Да', 'да', '+'):
            if user.last_summ and user.last_category:
                try:
                    user.request_make_record().json()
                except Exception as err:
                    raise Exception from err

                self.user_total_records(user, context)
                user.last_category = None
                user.last_summ = None

            elif not user.last_summ and user.last_category:
                if user.last_message.lower() not in user_categories:
                    self.user_create_category(
                        user, user.last_category, 'POST', context)
                    user.last_category = None
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
        elif user.last_message.lower().startswith('from:'):
            custom_period = user.last_message.lower().split(':')[1]
            self.user_total_records(
                user, context, period=custom_period, custom=custom_period
            )

        else:
            context.bot.send_message(
                chat_id=user.id,
                text='Я вас не понимаю, выберете категорию расхода',
                reply_markup=button_user_categories(user_categories)
            )

        LOG.info(f'{user.id}: {user.first_name} - {user.last_message}')

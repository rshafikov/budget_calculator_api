import json
import os
import logging

import requests as r
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

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

updater = Updater(token=TOKEN)


CATEGORIES = (
    '🧀Продукты', '🌭На работе', '🍤Доставка', '🧋Кофе',
    '🚕Такси/Шеринг', '🚇Транспорт', '🏠Дом', '🙈ЖКХ',
    '🎁Подарки', '💵Долги', '👔Одежда', '🏥Здоровье',
    '🙊Животные', '🎲Развлечения', '😎Разное', '⚙️Меню'
)

TABLE_OF_CATEGORIES = [
    ['🧀Продукты', '🌭На работе', '🍤Доставка', '🧋Кофе'],
    ['🚕Такси/Шеринг', '🚇Транспорт', '🏠Дом', '🙈ЖКХ'],
    ['🎁Подарки', '💵Долги', '👔Одежда', '🏥Здоровье'],
    ['🙊Животные', '🎲Развлечения', '😎Разное', '⚙️Меню']
]

TABLE_MAIN_MENU = [
    ['Записать расход'],
    ['Cписок расходов за месяц'],
    ['Показать итоговую сводку'],
]
buttons_categories = ReplyKeyboardMarkup(
    TABLE_OF_CATEGORIES, resize_keyboard=True)

buttons_table = ReplyKeyboardMarkup(TABLE_MAIN_MENU, resize_keyboard=True)

buttons_ok = ReplyKeyboardMarkup([['ДА ✅', 'НАЗАД 🔙']], resize_keyboard=True)

user_dict = {}


class User:
    urls = {
        'auth': f'http://{URL}/auth/users/',
        'token': f'http://{URL}/auth/jwt/create/',
        'records': f'http://{URL}/records/',
        'total': f'http://{URL}/records/total-spend/',
    }

    def __init__(self, update):
        self.headers = {'Content-Type': 'application/json'}
        self.id = update.effective_chat.id
        self.first_name = update.message.chat.first_name
        self.last_name = update.message.chat.last_name
        self.username = self.first_name + str(self.last_name)
        self.last_message = update.message.text
        self.last_summ = None
        self.last_category = None

    def get_auth(self):
        data = {
            'username': self.username,
            'password': str(self.id)+'ZSe!1'
        }
        data = json.dumps(data)
        self.request_auth = r.post(
            url=self.urls['auth'],
            headers=self.headers,
            data=data
        )
        self.request_token = r.post(
            url=self.urls['token'],
            headers=self.headers,
            data=data
        )
        self.token = 'Bearer ' + self.request_token.json().get('access')
        self.headers.update({'Authorization': self.token})

    def make_record(self):
        if self.last_summ and self.last_category:
            data = {
                'category': self.last_category,
                'amount': str(self.last_summ)
            }
            data = json.dumps(data)
            self.request_record = r.post(
                url=self.urls['records'],
                headers=self.headers,
                data=data
            )

    def get_total(self):
        self.request_total = r.get(
            url=self.urls['total'],
            headers=self.headers,
        )

    def get_records_list(self):
        self.request_records_list = r.get(
            url=self.urls['records'],
            headers=self.headers,
        )

    def __str__(self):
        return f'{self.username} -- {self.last_category}: {self.last_summ}'


def get_or_create_user(chat_id, update):
    if not user_dict.get(chat_id):
        user = User(update)
        user.get_auth()
        user_dict.update({user.id: user})
        return user

    return user_dict.get(chat_id)


def return_correct_date(string):
    new_string = string.split('T')
    date = new_string[0]
    time = new_string[1].split('.')[0]
    return f'🗓{date} 🕰{time}'


def make_table(list):
    table = [(
        '{0:<12} {1:>7} {2}\n'
        .format(
            CATEGORIES[record["category"] - 1],
            record["total"],
            USER_CURRENCY)
        ) for record in list
    ]
    return table


def start_message(update, context):
    chat_id = update.effective_chat.id
    user = get_or_create_user(chat_id, update)
    context.bot.send_message(
        chat_id=user.id,
        text=(
            'Привет, {}. Я буду следить за вашим семейным бюджетом. '
            'Указывай категорию расхода, вводи сумму, смотри итог.'
            .format(user.first_name)
        ),
        reply_markup=buttons_table
    )


def handle_message(update, context):
    chat_id = update.effective_chat.id
    user = get_or_create_user(chat_id, update)
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
                    f'Дата: {return_correct_date(record.get("created"))}\n'
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
        summary_list = ''.join(make_table(data.get('summary')))
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


updater.dispatcher.add_handler(CommandHandler('start', start_message))
updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

updater.start_polling()
updater.idle()

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

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='bot.log',
    filemode='a',
    level=logging.INFO
)

updater = Updater(token=TOKEN)


CATEGORIES = (
    '๐ง Products', '๐ญ Food', '๐ Transport', '๐ง Cofee',
    '๐ Taxi/Share', '๐  Home', '๐ฒ FUN', '๐ Presents',
    '๐ต Debts', '๐ Clothing', '๐ฅ Health', '๐ฉโ๐ Study',
    '๐ Everyday', '๐ ะะะฅ', '๐ Other', 'โ๏ธ ะะะะฎ'
)

TABLE_OF_CATEGORIES = [
    ['๐ง Products', '๐ญ Food', '๐ Transport', '๐ง Cofee'],
    ['๐ Taxi/Share', '๐  Home', '๐ฒ FUN', '๐ Presents'],
    ['๐ต Debts ', '๐ Clothing', '๐ฅ Health', '๐ฉโ๐ Study'],
    ['๐ Everyday', '๐ ะะะฅ', '๐ Other', 'โ๏ธ ะะะะฎ']
]

TABLE_MAIN_MENU = [
    ['ะะฐะฟะธัะฐัั ัะฐััะพะด'],
    ['Cะฟะธัะพะบ ัะฐััะพะดะพะฒ ะทะฐ ะผะตััั'],
    ['ะะพะบะฐะทะฐัั ะธัะพะณะพะฒัั ัะฒะพะดะบั'],
]
buttons_categories = ReplyKeyboardMarkup(
    TABLE_OF_CATEGORIES, resize_keyboard=True)

buttons_table = ReplyKeyboardMarkup(TABLE_MAIN_MENU, resize_keyboard=True)

buttons_ok = ReplyKeyboardMarkup([['ะะ โ', 'ะะะะะ ๐']], resize_keyboard=True)

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
    return f'๐{date} ๐ฐ{time}'


def make_table(list):
    table = [(
        '{0:<12} {1:>7} ััะฑ.\n'
        .format(CATEGORIES[record["category"] - 1], record["total"])
        ) for record in list
    ]
    return table


def start_message(update, context):
    chat_id = update.effective_chat.id
    user = get_or_create_user(chat_id, update)
    context.bot.send_message(
        chat_id=user.id,
        text=(
            'ะัะธะฒะตั, {}. ะฏ ะฑัะดั ัะปะตะดะธัั ะทะฐ ะฒะฐัะธะผ ัะตะผะตะนะฝัะผ ะฑัะดะถะตัะพะผ. '
            'ะฃะบะฐะทัะฒะฐะน ะบะฐัะตะณะพัะธั ัะฐััะพะดะฐ, ะฒะฒะพะดะธ ััะผะผั, ัะผะพััะธ ะธัะพะณ.'
            .format(user.first_name)
        ),
        reply_markup=buttons_table
    )


def handle_message(update, context):
    chat_id = update.effective_chat.id
    user = get_or_create_user(chat_id, update)
    user.last_message = update.message.text
    if user.last_message in ['ะะฐะฟะธัะฐัั ัะฐััะพะด', 'ะะะะะ ๐']:
        user.last_category = None
        user.last_summ = None
        context.bot.send_message(
            chat_id=chat_id,
            text='ะฃะบะฐะถะธัะต ะบะฐัะตะณะพัะธั ัะฐััะพะดะฐ, ะฟะพะถะฐะปัะนััะฐ',
            reply_markup=buttons_categories
        )
        logging.info(f'{user.id}: {user.first_name} - {user.last_message}')

    elif user.last_message == 'Cะฟะธัะพะบ ัะฐััะพะดะพะฒ ะทะฐ ะผะตััั':
        user.get_records_list()
        data = user.request_records_list.json()
        if data:
            context.bot.send_message(
                chat_id=chat_id,
                text=('\n'.join([
                    f'ะะฐัะฐ: {return_correct_date(record.get("created"))}\n'
                    f'ะะฐัะตะณะพัะธั: {record.get("category")}\n'
                    f'ะกัะผะผะฐ: {record.get("amount")} ััะฑ.\n' for record in data
                    ])
                )
            )
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text='ะ ััะพะผ ะผะตัััะต ะตัะต ะฝะต ะฑัะปะพ ัะฐััะพะดะพะฒ, ะทะฐะฟะธัะฐัั ัะฐััะพะด?',
                reply_markup=buttons_table
                )
            logging.info(f'{user.id}: {user.first_name} - {user.last_message}')

    elif user.last_message == 'ะะพะบะฐะทะฐัั ะธัะพะณะพะฒัั ัะฒะพะดะบั':
        user.get_total()
        data = user.request_total.json()
        summary_list = ''.join(make_table(data.get('summary')))
        total_per_day = data.get("current_day")
        if not total_per_day:
            total_per_day = 0
        context.bot.send_message(
            chat_id=chat_id,

            text=(
                f'ะะฐ ะฒัะต ะฒัะตะผั: {data.get("total")} ััะฑ.\n'
                f'ะะฐัะธ ัะฐััะพะดั ะทะฐ ะผะตััั: {data.get("current_month")} ััะฑ.\n'
                f'ะะฐัะธ ัะฐััะพะดั ะทะฐ ะดะตะฝั: {total_per_day} ััะฑ.\n'
                'ะะฐัะตะณะพัะธั    |    ะขะพัะฐะป    \n'
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
                text='ะฃะบะฐะถะธัะต ััะผะผั:'
            )

    elif user.last_message == 'โ๏ธ ะะะะฎ':
        context.bot.send_message(
            chat_id=chat_id,
            text='ะัะฑะตัะตัะต ะดะตะนััะฒะธะต',
            reply_markup=buttons_table
        )

    elif user.last_message.isdigit():
        user.last_summ = user.last_message
        if user.last_category:
            context.bot.send_message(
                chat_id=chat_id,
                text=(
                    f'ะั ัะบะฐะทะฐะปะธ: \n'
                    '------------\n'
                    f'ะะฐัะตะณะพัะธั: {user.last_category}\n'
                    f'Cัะผะผะฐ: {user.last_message} ััะฑ.\n\n'
                    'ะัะปะธ ะฒะตัะฝะพ, ะฝะฐะถะผะธัะต "ะะ โ"'
                ),
                reply_markup=buttons_ok
            )
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text='ะฃะบะฐะถะธัะต ะบะฐัะตะณะพัะธั ัะฐััะพะดะฐ, ะฟะพะถะฐะปัะนััะฐ',
                reply_markup=buttons_categories
            )

    elif user.last_message == 'ะะ โ':
        if user.last_summ and user.last_category:
            user.make_record()
            context.bot.send_message(
                chat_id=chat_id,
                text=(
                    'ะะฐะฟะธัะฐะฝั ะดะฐะฝะฝัะต: โ\n'
                    f'ะะฐัะตะณะพัะธั: {user.last_category}\n'
                    f'ะกัะผะผะฐ: {user.last_summ} ััะฑ.\n\n'
                    f'ะะถะธะดะฐั ะฝะพะฒัั ะทะฐะฟะธัั :)'),
                reply_markup=buttons_table
            )
            user.last_category = None
            user.last_summ = None
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text='ะฃะบะฐะถะธัะต ััะผะผั:'
            )

    else:
        context.bot.send_message(
            chat_id=chat_id,
            text='ะฏ ะฒะฐั ะฝะต ะฟะพะฝะธะผะฐั, ะฒัะฑะตัะตัะต ะบะฐัะตะณะพัะธั ัะฐััะพะดะฐ',
            reply_markup=buttons_categories
        )


updater.dispatcher.add_handler(CommandHandler('start', start_message))
updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

updater.start_polling()
updater.idle()

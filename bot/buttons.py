from telegram import ReplyKeyboardMarkup

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
    ['Записать расход', 'Отчеты'],
    ['Список расходов', 'Выбрать валюту'],
]
TABLE_REPORTS = [
    ['Отчет за месяц'],
    ['Отчет за неделю'],
    ['Отчет за день'],
]
TABLE_CURRENCY = [
    ['EUR'],
    ['RUB'],
    ['USD'],
    ['USDT'],
]

BUTTON_TABLE = ReplyKeyboardMarkup(TABLE_MAIN_MENU, resize_keyboard=True)
BUTTON_OK = ReplyKeyboardMarkup([['ДА ✅', 'НАЗАД 🔙']], resize_keyboard=True)
BUTTON_REPORTS = ReplyKeyboardMarkup(TABLE_REPORTS, resize_keyboard=True)
BUTTON_CURRENCY = ReplyKeyboardMarkup(TABLE_CURRENCY, resize_keyboard=True)

def button_user_categories(buttons: list) -> ReplyKeyboardMarkup:
    button_row = []
    button_matrix = []
    for button in buttons:
        if len(button_row) <= 3:
            button_row.append(button)
        else:
            button_matrix.append(button_row)
            button_row = []
            button_row.append(button)
    if button_row:
        button_matrix.append(button_row)
    return ReplyKeyboardMarkup(button_matrix, resize_keyboard=True)

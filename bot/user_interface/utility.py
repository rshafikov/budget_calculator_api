from variables import USER_CURRENCY, logging
# from tabulate import tabulate
import re
import json
from prettytable import PrettyTable, ALL

LOG = logging.getLogger(__name__)

def return_correct_date(date_string):
    new_string = date_string.split('T')
    date = new_string[0]
    time = new_string[1].split('.')[0]
    return f'🗓{date} 🕰{time}'


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def prettify_total(data, cur):
    period = data["period"]

    markdown_text = f'<pre>'
    markdown_text += f'Period: {period}\n'

    total_per_p = data["total_per_period"]
    table = PrettyTable()
    table.field_names = ["CATEGORY", cur, "%"]
    for item in data['summary']:
        category = item['category__category_name']
        money = round(item['total'])
        total_share = round(money / total_per_p * 100)
        table.add_row([category, money, total_share])
    table.add_row(["TOTAL", round(total_per_p), 100])

    # Настройки отображения таблицы
    # В строке telegram помещается 31 символ
    table._max_width = {"CATEGORY": 11, cur: 7, "%": 3}
    table.hrules = ALL
    table.align = "l"
    # table.reversesort = True

    markdown_text += table.get_string(sortby=cur)
    markdown_text += f'</pre>'

    return markdown_text
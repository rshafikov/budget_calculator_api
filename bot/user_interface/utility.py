import traceback
from datetime import datetime
from functools import wraps

from prettytable import ALL, PrettyTable
from variables import USER_CURRENCY, logging

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
    output = f'<b>Period: {data["period"]}</b>\n<pre>'
    # В строке telegram помещается 31 символ, max_width == 31
    table = PrettyTable(
        hrules=ALL,
        align='l',
        field_names=["CATEGORY", cur, "%"],
        # reversesort=True
    )
    table._max_width = {"CATEGORY": 11, cur: 7, "%": 3}

    for item in data['summary']:
        category = item['category__category_name']
        money = round(item['total'], 2)
        total_share = round(money / data["total_per_period"] * 100)
        table.add_row([category, money, total_share])
    table.add_row(["TOTAL", round(data["total_per_period"], 1), 100])
    output += table.get_string(sortby=cur) + '</pre>'
    return output


def execute_time_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            start_time = datetime.utcnow()
            func(*args, **kwargs)
            delta = datetime.utcnow() - start_time
            LOG.info(
                'Func: {}. Execute time: {} '.format(func.__name__, delta))
        except Exception as error:
            LOG.error((
                'There is an error with {}'.format(func.__name__),
                'Error: {}'.format(error),
                'Full error: {}'.format(traceback.format_exc())))

    return wrapper

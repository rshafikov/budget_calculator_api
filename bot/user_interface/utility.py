from variables import USER_CURRENCY, logging
# from tabulate import tabulate
import re
import json

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


def prettify(data):
    period = data["period"]
    st_p = " " * (13 - len(period))
    markdown_text = (
        '<pre>'
        f'|        Period: {period}{st_p}|\n'
        f'| --------------------------- |\n'
        f'|   Category   |   Expenses   |\n'
        f'| ------------ | ------------ |\n'
    )
    for item in data['summary']:
        category = item['category__category_name']
        total = str(item['total'])
        if len(category) > 14:
            category = category[:13]
        sp_cat = " " * (11 - len(category))
        sp_tot = " " * (10 - len(total))
        cur = "€"
        markdown_text += f'|   {category}{sp_cat}|   {total}{cur}{sp_tot}|\n'
    markdown_text += '</pre>'
    return markdown_text

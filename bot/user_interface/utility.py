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


def prettify_total(data, cur):
    p = data["period"]
    total_per_p = data["total_per_period"]
    total_per_p = (f"{float(total_per_p):.0f}" if cur == 'RUB' else
                   f"{float(total_per_p):.1f}")
    st_p = " " * (13 - len(p))
    markdown_text = (
        '<pre>'
        f'+--------------+--------------+\n'
        f'|        Period: {p}{st_p}|\n'
        f'+--------------+--------------+\n'
        f'|   Category   |   Expenses   |\n'
        f'+--------------+--------------+\n'
    )
    for item in data['summary']:
        category = item['category__category_name']
        total = (
            f"{float(item['total']):.0f}" if cur == 'RUB' else
            f"{float(item['total']):.1f}")
        if len(category) > 14:
            category = category[:13]
        sp_cat = " " * (11 - len(category))
        sp_tot = " " * (7 - len(total))
        sp_totp = " " * (9 - len(total_per_p))
        markdown_text += f'|   {category}{sp_cat}|   {total} {cur}{sp_tot}|\n'
    markdown_text += (
        f'+--------------+--------------+\n'
        f'|         Total: {total_per_p} {cur}{sp_totp}|\n'
        f'+--------------+--------------+\n'
        '</pre>'
    )
    return markdown_text




from variables import USER_CURRENCY
# from tabulate import tabulate


def return_correct_date(date_string):
    new_string = date_string.split('T')
    date = new_string[0]
    time = new_string[1].split('.')[0]
    return f'🗓{date} 🕰{time}'


# def make_table(records_list):
#     headers = ["Category", "Total", "Currency"]
#
#     records_list = [
#         {"category__category_name": "Category1", "total": 100},
#         {"category__category_name": "Category2", "total": 200},
#         {"category__category_name": "Category3", "total": 300},
#     ]
#     formatted_rows = []
#
#     for record in records_list:
#         formatted_row = f"{record['category__category_name']:<12} {record['total']:<7} {USER_CURRENCY}"
#         formatted_rows.append(formatted_row)
#     return "\n".join(formatted_rows)


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

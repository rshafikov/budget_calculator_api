from variables import USER_CURRENCY


def return_correct_date(date_string):
    new_string = date_string.split('T')
    date = new_string[0]
    time = new_string[1].split('.')[0]
    return f'🗓{date} 🕰{time}'


def make_table(records_list):
    table = [(
        '{0:<12} {1:>7} {2}\n'
        .format(
            record['category__category_name'],
            record['total'],
            USER_CURRENCY)
    ) for record in records_list]
    return table
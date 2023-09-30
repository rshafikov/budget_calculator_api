import prettytable as pt
x = pt.PrettyTable()

x.field_names = ["CATEGORY", "$RUB", "%"]
x.add_rows(
    [
        ["Adelaide", 1295, 1],
        ["Brisbane", 59051245, 151],
        ["Darwin", 112, 13],
        ["Hobart", 1357, 15],
        ["Sydney", 2058, 3],
        ["Melbournecitymfakabigstring", 1566, 7],
        ["Perth", 5386, 5],
    ]
)

# В строке telegram помещается 31 символ
x._max_width = {"CATEGORY": 12, "$RUB": 7, "%": 2}
x.hrules=pt.ALL
x.align = "l"
x.reversesort = True
mystring = x.get_string(sortby="$RUB")

print(mystring)
from db_tiny import get_all_symbols, is_symbol_present, add_average_delivery

symbols = get_all_symbols()

# count = 0
for stock in symbols:
    name = stock['name']

    if name[0] < 'E':
        continue
    print('Working with ', name)

    if is_symbol_present(name):
        add_average_delivery(name)
    

    
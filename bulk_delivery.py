from db import get_all_symbols, is_symbol_present, check_symbol_date
from delivery_download import download_data, save
from datetime import date
from time import sleep

symbols = get_all_symbols()
# print(symbols)

failed_count = 0

# count = 0
for stock in symbols:
    name = stock['name']

    # if is_symbol_present(name):
    # # if name[0] < 'P':
    #     # print('Skipping', name)
    #     continue

    is_present = check_symbol_date(name, '28-Feb-2024')

    if is_present:
        continue

    print('Working with ', name)

    # count += 1

    # if count == 5:
    #     break
    # continue

    try:
        start_date = date(day=9, month=2, year=2024)
        end_date = date(day=28, month=2, year=2024)
        save(symbol=name, start_date=start_date, end_date=end_date)
        sleep(3)
        failed_count = 0

        if failed_count == 5:
            print('Getting excpetions, breaking.....')
            break
    except:
        print('Excpeption occurred with ', name)
        failed_count += 1
    print('\n\n\n')
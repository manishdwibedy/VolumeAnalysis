from db import get_symbol_data, check_symbol_date


data = get_symbol_data('HDFCBANK')

for day in data:
    delivery = day.get('COP_DELIV_PERC', 'N.A.')
    
    average = day.get('Rolling_Delivery', 'N.A.')
    date = day['mTIMESTAMP']
    print(f"{day.get('CH_SYMBOL')} {date} - {delivery} - {average}")

# is_present = check_symbol_date('HDFCBANK', '28-Feb-2023')
# print(is_present)

# import pandas as pd

# df = pd.DataFrame(data)
# df.to_csv('my_data.csv', index=False)

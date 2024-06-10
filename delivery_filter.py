
from db import get_all_symbols, is_symbol_present, count_window_average
from delivery_download import download_data, save
from datetime import date
from time import sleep
import pickle

read_pickle = True

if not read_pickle:
    symbols = get_all_symbols()



    filter_map = {}
    for stock in symbols:
        name = stock['name']

        print(' Working with ', name)
        min_diff = 5
        window=30
        count, df = count_window_average(name, window=window, min_diff=min_diff,get_rows=True)
        
        if count in filter_map:
            filter_map[count].append(df)
        else:
            filter_map[count] = [df]

    with open("delivery_filter.p", "wb") as file:
        # Write the "student" dictionary to the file
        pickle.dump(filter_map, file)

else:
    # Read from a pickle file
    with open('delivery_filter.p', 'rb') as f:
        filter_map = pickle.load(f)
    top_count = 10

    new_dict = {key: value for key, value in filter_map.items() if key is not None}

    top_keys_list = sorted(new_dict.keys(), reverse=True)[10:11]

    print(top_keys_list)


    # top_keys = sorted(filter_map.keys(), reverse=True, key=lambda x: filter_map[x])[:top_count]

    for count in top_keys_list:
        print(f"With {count} delivery difference")
        for df in filter_map[count]:
            print(df)

        input('Press key to continue')

"""
129  ZFCVINDIA           84.92  07-Feb-2024         61.787000  23.133000
Press key to continue
With 13 delivery difference
    CH_SYMBOL  COP_DELIV_PERC   mTIMESTAMP   CA  Rolling_Delivery       Diff
105     AARVI           64.07  03-Jan-2024  NaN         56.324667   7.745333
107     AARVI           66.95  05-Jan-2024  NaN         56.432667  10.517333
111     AARVI           69.72  11-Jan-2024  NaN         57.978000  11.742000
113     AARVI           76.37  15-Jan-2024  NaN         59.714333  16.655667
"""
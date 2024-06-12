import pandas as pd
from pandas import read_excel
import os
from db import save_symbols

# Read from 
# https://www.nseindia.com/regulations/listing-compliance/nse-market-capitalisation-all-companies
# 

def read():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    my_sheet = 'Sheet1' 
    file_name = 'MCAP28032024.xlsx' 
    
    df = read_excel(dir_path + "/" + file_name, sheet_name = my_sheet)
    
    df.columns.values[3] = "Market capitalization"

    print(df.head().to_dict('records'))

    return df.to_dict('records')


save_symbols(read())
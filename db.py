# from tinydb import TinyDB, Query
# import pandas as pd

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import os
from dotenv import load_dotenv

load_dotenv()

MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_HOST = os.getenv('MONGO_HOST')

print(MONGO_HOST, MONGO_USERNAME, MONGO_PASSWORD)
URI = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}/?retryWrites=true&w=majority&appName=VolumeAnalysis"
# client = pymongo.MongoClient()

client = MongoClient(URI, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["volume_analysis"]
symbols = db['symbols']
stock_data = db["stock_data"]


def save_symbols(symbol_list):
    result = symbols.insert_many(symbol_list)
    return result.inserted_ids

def get_all_symbols():
    symbols = stock_data.find()
    return symbols

def get_symbol_data(symbol):
    query = { "symbol": symbol }

    doc = stock_data.find(query)

    return doc

def remove_symbol_data(symbol):
    table = db.table('data')
    symbol_data = Query()
    data = table.remove(symbol_data.CH_SYMBOL == symbol)

    return data

def save_data(data_list):
    result = stock_data.insert_one(data_list)
    return result


def check_symbol_date(symbol, check_date):
    table = db.table('data')
    symbol_data = Query()
    data = table.search(symbol_data.CH_SYMBOL == symbol)

    for day in data:
        delivery = day.get('COP_DELIV_PERC', 'N.A.')
        
        average = day.get('Rolling_Delivery', 'N.A.')
        date = day['mTIMESTAMP']

        if date == check_date:
            return True
    
    return False


def add_average_delivery(symbol, window=30):
    table = db.table('data')
    symbol_data = Query()
    data = table.search(symbol_data.CH_SYMBOL == symbol)

    df = pd.DataFrame(data)
    df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], format='mixed')
    df['COP_DELIV_PERC'] = pd.to_numeric(df['COP_DELIV_PERC'], errors='coerce')
    df.sort_values(by='TIMESTAMP', ascending=True, inplace=True)
    
    df['Rolling_Delivery'] = df['COP_DELIV_PERC'].rolling(window=window).mean()

    table.remove(symbol_data.CH_SYMBOL == symbol)

    df['TIMESTAMP'] = df['TIMESTAMP'].astype(str)

    table.insert_multiple(df.to_dict(orient='records'))

def get_data(symbol):
    table = db.table('data')
    symbol_data = Query()
    data = table.search(symbol_data.CH_SYMBOL == symbol)

    return data

def is_symbol_present(symbol):
    table = db.table('data')
    symbol_data = Query()
    data = table.search(symbol_data.CH_SYMBOL == symbol)

    return len(data) > 0

def count_window_average(symbol, min_diff=5, window=5, get_rows=False):
    table = db.table('data')
    symbol_data = Query()
    data = table.search(symbol_data.CH_SYMBOL == symbol)

    if len(data) == 0:
        return None, None
    
    # print(data)
    df = pd.DataFrame(data)
    df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])
    df.sort_values(by='TIMESTAMP', ascending=True, inplace=True)

    window_df = df.tail(window)
    # window_df['Diff'] = window_df['COP_DELIV_PERC'] - window_df['Rolling_Delivery']
    window_df = window_df.copy()
    window_df.loc[:, 'Diff'] = window_df['COP_DELIV_PERC'] - window_df['Rolling_Delivery']

    count = (window_df['Diff'] > min_diff).sum()

    filtered_df = None
    if get_rows:
        
        filtered_df = window_df[window_df['Diff'] > min_diff]
        cols_to_drop = [0, 2,3,	4,	5,	6,	7,	8,	9,	10,	11,	12,	13,	14,15,16,17,18,19,20,21,23]
        filtered_df = filtered_df.copy()

        filtered_df.drop(filtered_df.columns[cols_to_drop], axis=1, inplace=True)

    return count, filtered_df

def count_above_average(symbol, min_diff=5):
    table = db.table('data')
    symbol_data = Query()
    data = table.search(symbol_data.CH_SYMBOL == symbol)

    count = 0
    for day_info in data:
        delivery = day_info['COP_DELIV_PERC']
        average_delivery = day_info['Rolling_Delivery']
        date = day_info['mTIMESTAMP']
        if delivery - average_delivery > min_diff:
            print(f"{date} - {delivery} - {average_delivery}")
            count += 1

    return count
# add_average_delivery('ITC')

# print(get_all_symbols())
# remove_symbol_data('PAGEIND')
# print(is_symbol_present('ITC'))
# data = get_symbol_data('IBULHSGFIN')
# for day in data:
#     delivery = day['COP_DELIV_PERC']
#     average = day.get('Rolling_Delivery', 'N.A.')
#     date = day['mTIMESTAMP']
#     print(f"{date} - {delivery} - {average}")

# print(count_above_average('ITC'))

# data = get_data('ITC')

# for day in data:
#     delivery = day['COP_DELIV_PERC']
#     average = day.get('Rolling_Delivery', 'N.A.')
#     date = day['mTIMESTAMP']
#     print(f"{date} - {delivery} - {average}")

# count, df = count_window_average('SBIN', window=30, get_rows=True)
# print(count)
# print(df)
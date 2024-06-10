from nsepython import nsefetch
import pandas as pd

def equity_history(symbol,series,start_date,end_date):
    payload = nsefetch("https://www.nseindia.com/api/historical/cm/equity?symbol="+symbol+"&series=[%22"+series+"%22]&from="+start_date+"&to="+end_date+"")
    return pd.DataFrame.from_records(payload["data"])

symbol = "SBIN"
series = "EQ"
start_date = "01-01-2024"
end_date ="31-01-2024"
data = equity_history(symbol,series,start_date,end_date)
print(data)

# works - BUT NO DELIVERY DATA
# from datetime import date
# from jugaad_data.nse import bhavcopy_save, bhavcopy_fo_save

# # Download bhavcopy
# # bhavcopy_save(date(2020,1,1), "/path/to/directory")

# # # Download bhavcopy for futures and options
# # bhavcopy_fo_save(date(2020,1,1), "/path/to/directory")

# # Download stock data to pandas dataframe
# from jugaad_data.nse import stock_df
# df = stock_df(symbol="SBIN", from_date=date(2024,1,1),
#             to_date=date(2024,1,30), series="EQ")

# print(df)
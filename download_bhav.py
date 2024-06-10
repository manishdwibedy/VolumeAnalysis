#  works - BUT NO DELIVERY DATA
from datetime import date, timedelta
from jugaad_data.nse import bhavcopy_save, bhavcopy_fo_save
from time import sleep
# Download bhavcopy
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

start_date = date(year=2024, month=2, day=3)
end_date = date(year=2024, month=2, day=10)
delta = timedelta(days=1)

current_date = start_date
while current_date <= end_date:
    location = dir_path + "/bhavcopy"
    print(location)
    try:
        bhavcopy_save(current_date, location)
    except:
        print('holiday or weekend')
    current_date += delta
    sleep(1)
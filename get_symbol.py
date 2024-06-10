import pandas as pd
import os
from db import save_symbols

dir_path = os.path.dirname(os.path.realpath(__file__))

df = pd.read_csv(dir_path + "/bhavcopy/cm01Feb2024bhav.csv")

eq_symbols = df[df["SERIES"] == "EQ"]["SYMBOL"]

save_symbols(list(eq_symbols))
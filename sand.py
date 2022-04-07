import pandas as pd
import sys

try:
    fname = sys.argv[1]
except:
    fname = 'merged.csv'

df_raw = pd.read_csv(fname)

def dropped_nan_views(df):
    columns = [str(monthno) for monthno in range(1, 13)]
    return df.dropna(axis=0, subset=columns)

df = dropped_nan_views(df_raw)

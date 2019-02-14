import pandas as pd

COLS_ZERO = ['Price_RO', 'Price_HU', 'Price_SK', 'Price_CZ', 'Price_GER', 'Price_FR']

df = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/data/data_15-18_price_normal.csv', parse_dates=['Date'], header=0)

for column in COLS_ZERO:
    df.loc[df[column] < 0, column] = 0

df.to_csv('/media/cristi/DATA/projects/inflectionPoint/data/data_15-18_price_zeroed_test.csv', index=False)
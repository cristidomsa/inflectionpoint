import pandas as pd

df = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/entsoe/prices_hu_ro.csv', 
                index_col=[0], 
                parse_dates=[0], 
                date_parser=lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

df.resample('1D').agg({'Price_RO': 'mean',
                       'Price_HU': 'mean'}).to_csv('prices_hu_ro_zi.csv')
import pandas as pd

HEADERS = ['Date', 'Price_CZ', 'Price_FR', 'Price_GER', 'Price_HU', 'Price_SK']

content = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/entsoe/nov.csv', 
                          delimiter=',', 
                          header=0,
                          index_col='Date',
                          names=HEADERS,
                          parse_dates=['Date'],
                          date_parser=lambda x: pd.datetime.strptime(x.split(' - ')[0], '%d.%m.%Y %H:%M'), 
                          infer_datetime_format=True
                         )

content.to_csv('price_nov.csv')

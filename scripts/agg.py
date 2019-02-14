from os import path
from datetime import datetime
from holiday_scraper import get_holidays

import pandas as pd

COLS_PRICE = ['Traded_RO', 'Traded_RO_buy', 'Traded_RO_sell']
COLS_CROSS = ['Price_RO', 'Price_HU', 'Price_SK', 'Price_CZ', 'RO_HU', 'HU_RO', 'HU_SK', 'SK_HU', 'SK_CZ', 'CZ_SK']
COLS_ZERO = ['Price_GER', 'Price_FR', 'Price_RO', 'Price_HU', 'Price_SK', 'Price_CZ']

def get_content(file, type='entsoe'):

    return pd.read_csv(file, 
                    delimiter=',')

def write_data(content, file):
    content.to_csv(file, encoding='utf-8', index=True)

def make_zeros(df):
    num = df._get_numeric_data()
    num[num < 0] = 0

holi = get_holidays()

zeroed = True
data_all = pd.DataFrame()

for year in range(2015,2019):
    result = None
    
    print('=======================')
    print(year)
    base_content = get_content(path.abspath(path.join('../entsoe', 'entsoe_{}.csv'.format(year))))
    ro_content = get_content(path.abspath(path.join('../opcom', 'opcom_{}.csv'.format(year))))
    cross_content = get_content(path.abspath(path.join('../opcom/cross/', 'opcom_cross_{}.csv'.format(year))))

    try:
        for column in COLS_CROSS:
            base_content[column] = cross_content[column]
            print(column, '- Done')
        for column in COLS_PRICE:
            base_content[column] = ro_content[column]
            print(column, '- Done')

        if zeroed:
            for column in COLS_ZERO:
                base_content.dropna(inplace=True)
                base_content[column] = pd.to_numeric(base_content[column], errors='coerce')
                base_content.loc[base_content[column] < 0, column] = 0

        for cnt in holi.keys():
            base_content['Holiday_{}'.format(cnt)] = base_content['Date'].apply(lambda x: x.split(' ')[0] in holi[cnt])
            print('Holiday_{} - Done'.format(cnt))

        base_content = base_content.reset_index(drop=True)
        base_content = base_content.set_index('Date')
        base_content.index = pd.to_datetime(base_content.index)
        base_content['Quarter'] = base_content.index.to_period('Q')
        print('Quarters - Done'.format(cnt))
        base_content['Weekend'] = base_content.index.dayofweek // 5 == 1
        print('Weekends - Done'.format(cnt))

        write_data(base_content, path.abspath(path.join('../data/', 'entsoe_opcom_cross_zeroed_price_{}.csv'.format(year))))
        data_all = data_all.append(base_content)
    except Exception as e:
        print(e, '- Error!')
    

write_data(data_all, '../data/prices.csv')
from os import path
import pandas as pd

COLS = ['Price_RO', 'Price_HU', 'Price_SK', 'Price_CZ', 'RO_HU', 'HU_RO', 'HU_SK', 'SK_HU', 'SK_CZ', 'CZ_SK']

def get_content(file, type='entsoe'):

    
    return pd.read_csv(file, 
                    delimiter=',')

def write_data(content, file):
    content.to_csv(file, encoding='utf-8', index=True)

for year in range(2015,2019):
    result = None
    print(year)
    base_content = get_content(path.abspath(path.join('../data/', 'entsoe_opcom_{}.csv'.format(year))))
    cross_content = get_content(path.abspath(path.join('../opcom/cross/', 'opcom_cross_{}.csv'.format(year))))

    try:
        for column in COLS:
            base_content[column] = cross_content[column]
            print(column, '- Done')
    except Exception as e:
        print(e, '- Error!')
    write_data(base_content, path.abspath(path.join('../data/', 'entsoe_opcom_cross_{}.csv'.format(year))))
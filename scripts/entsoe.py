from datetime import timedelta, date, time, datetime
import wget
import httplib2
import csv
import re
from os import path
import pandas as pd
import numpy as np

HEADERS = ['Date', 'Price']
HEADERS_AGG = ['Price_FR', 'Price_GER']
DTYPES = [str, float]
PATH = path.abspath('../entsoe')

COUNTRIES = ['FR', 'GER']

def get_content(file):
    content = pd.read_csv(file, 
                          delimiter=',', 
                          header=None, 
                          skiprows=1, 
                          names=HEADERS, 
                          index_col='Date', 
                          parse_dates=['Date'],
                          date_parser=lambda x: pd.datetime.strptime(x.split(' - ')[0], '%d.%m.%Y %H:%M'), 
                          infer_datetime_format=True)

    return content

def transform_data(content, country):

    return content.rename(index=str, columns={"Price": "Price_{}".format(country)})
    
def write_data(content, file):
    content[HEADERS_AGG].dropna().to_csv(file, encoding='utf-8', index=True)

for year in range(2018,2019):
    result = None
    print(year)
    for cnt in COUNTRIES:

        content = get_content(path.join(PATH, cnt, 'Day-ahead Prices_{}01010000-{}01010000_{}.csv'.format(year, year+1, cnt)))
        content = transform_data(content, cnt)
        #write_data(content, path.join(PATH, 'entsoe_{}_test.csv'.format(year)))
        try:
            result = result.merge(content, on='Date')
            print(cnt, '- Done')
        except AttributeError:
            result = content
            print(cnt, '- First!')
        except Exception as e:
            print(cnt, '- Error!')
    write_data(result, path.join(PATH, 'entsoe_{}.csv'.format(year)))
    
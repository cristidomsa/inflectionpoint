from datetime import timedelta, date, time, datetime
import wget
import httplib2
import csv
import re
from os import path
import pandas as pd
import numpy as np

HEADERS = ['Date', 'Consum', 'Medie_Consum', 'Prod_total', 'Prod_Carbune', 'Prod_Hidrocarburi', 'Prod_Ape','Prod_Nuclear','Prod_Eolian','Prod_Foto','Prod_Biomasa','Sold']
DTYPES = [str, float, float, float, float, float, float, float, float, float, float, float]
SRC_PATH = path.abspath('../transelectrica/original/csv')
DEST_PATH = path.abspath('../transelectrica/')

DATA = {}

def get_content(file):

    dateparse = lambda x: pd.datetime.strptime(str(x), '%d-%m-%Y %H:%M:%S')

    content = pd.read_csv(file, 
                          delimiter=',', 
                          header=None, 
                          skiprows=1, 
                          names=HEADERS, 
                          index_col='Date', 
                          parse_dates=['Date'], 
                          date_parser = dateparse,
                          infer_datetime_format=True)

    return content

def make_zeros(df):
    num = df._get_numeric_data()
    num[num < 0] = 0

def transform_data(content):

    for col in HEADERS[1:]:
        content[col] = content[col].apply(pd.to_numeric, errors='coerce')

    return content.resample('1H').agg({'Consum': 'mean',
                                    #   'Prod_total': 'mean',
                                    #  'Prod_Carbune': 'mean',
                                    #  'Prod_Hidrocarburi': 'mean',
                                    #  'Prod_Ape': 'mean',
                                    #  'Prod_Nuclear': 'mean',
                                    #  'Prod_Eolian': 'mean',
                                    #  'Prod_Foto': 'mean',
                                    #  'Prod_Biomasa': 'mean',
                                    #  'Sold': 'mean'
                                     })

def write_data(content, file):
    content.reset_index().to_csv(file, encoding='utf-8', index=False)

data_full = pd.DataFrame()

for year in [2015,2016,2017,2018]:
    
    content = get_content(path.join(SRC_PATH, 'ROM production {}.csv'.format(year)))
    #content = get_content('trans.csv')
    try:
        data = transform_data(content)
        #write_data(data, path.join(DEST_PATH, 'transelectrica_{}.csv'.format(year)))
        data_full = data_full.append(data)
        print(year, '- Done')
    except:
        print(year, '- Error!')
    
write_data(data_full, '../data/consum.csv')

    
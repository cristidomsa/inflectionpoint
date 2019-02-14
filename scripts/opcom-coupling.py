from datetime import timedelta, date, time, datetime
import wget
import httplib2
import requests
import csv
import re
import os
import pandas as pd

URL = "https://www.opcom.ro/rapoarte/pzu/export_csv_RaportMarketResults.php?zi={}&luna={}&an={}&limba=en"
DELIMITERS = ',', '\r', '\n'
HEADERS = ['Interval', 'Price_RO', 'Price_HU', 'Price_SK', 'Price_CZ', 'RO_HU', 'HU_RO', 'HU_SK', 'SK_HU', 'SK_CZ', 'CZ_SK', 'Available_RO_HU', 'Available_HU_RO', 'Available_HU_SK', 'Available_SK_HU', 'Available_SK_CZ', 'Available_CZ_SK']
DROP_COL = ['Interval', 'Available_RO_HU', 'Available_HU_RO', 'Available_HU_SK', 'Available_SK_HU', 'Available_SK_CZ', 'Available_CZ_SK']
PATH = '../opcom/cross/{}/'
BASE_PATH = '../opcom/cross/'

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def get_file(single_date):
    print('making request')
    r = requests.post(URL.format(single_date.day, single_date.month, single_date.year))
    #TODO: Yeti sez: PUTOARE
    filename = r.headers['Content-disposition'].split('filename=')[-1].replace('/', '_')

    print(filename, r.status_code)

    return filename, r.content

def write_file(content, filename, year):

    filepath = os.path.abspath(os.path.join(PATH.format(year), filename))

    with open(filepath, 'wb') as f:
        f.write(content)
    
    print(filename, '-done.')
    return content

def read_values(content):
    pattern =  r"delivery day: (\d+\/\d+\/\d{4})"

    matches = re.finditer(pattern, content, re.MULTILINE)

    for matchNum, match in enumerate(matches):        
        
        date = match.group(1).strptime('%m/%d/%Y')

    # #TODO: Clear code
    # values = re.finditer(append(datetime.combine(date,time(int(content[1])-1)).strftime("%Y-%m-%d %H:%M"))
    
    for v in content[2:4]:
        values.append(v)
    return values

def get_old_data(start_date=date(2007, 1, 1), end_date=date(2019, 1, 1)):

    for single_date in daterange(start_date, end_date):

        fn, content = get_file(single_date)
        write_file(content, fn, single_date.year)


def transform_data(year):

    start_date = date(year, 1, 1)
    if year == 2018:
        end_date = date.today()+timedelta(days=1)
    else:
        end_date = date(year+1, 1, 1)

    result = pd.DataFrame()

    for day in daterange(start_date, end_date):
        path = os.path.abspath(os.path.join(PATH.format(year), 'MarketCouplingResults_{}_{}_{}.csv'.format(day.month, day.day, year)))
        print(path)

        content = pd.read_csv(path, 
                          delimiter=',', 
                          header=None, 
                          skiprows=23,
                          names=HEADERS)

        result = result.append(content)
    result = result.drop(columns=DROP_COL)
    result.to_csv(os.path.abspath(os.path.join(BASE_PATH,'opcom_cross_{}.csv'.format(year))), index=False, encoding='utf-8')

start_date = date(2018, 12, 11)
end_date = date.today() + timedelta(days=1)

get_old_data(start_date, end_date)
for year in range(2015, 2019):
    transform_data(year)
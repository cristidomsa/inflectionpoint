from datetime import timedelta, date, time, datetime
import wget
import httplib2
import requests
import csv
import re
import os
import pandas as pd

URL = "https://www.opcom.ro/rapoarte/pzu/export_csv_PIPsiVolTranNOU.php?zi={}&luna={}&an={}&limba=en"
DELIMITERS = ',', '\r', '\n'
HEADERS = ['Trading_Zone', 'Interval', 'Traded_RO', 'Traded_RO_buy', 'Traded_RO_sell']
PATH = '../opcom/price/{}/'
BASE_PATH = '../opcom/'

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def get_file(single_date):
    r = requests.post(URL.format(single_date.day, single_date.month, single_date.year))
    #TODO: Yeti sez: PUTOARE
    filename = r.headers['Content-disposition'].split('filename=')[-1].replace('/', '_')

    return filename, r.content

def write_file(content, file, year):

    filepath = os.path.abspath(os.path.join(PATH.format(year), file))

    with open(filepath, 'wb') as f:
        f.write(content)
    return content

def transform_date(row):
    pass

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

def get_old_data(start_date=date(2018, 11, 1), end_date=date.today() + timedelta(days=1)):

    for single_date in daterange(start_date, end_date):

        fn, content = get_file(single_date)
        write_file(content, fn, single_date.year)


def transform_data(year):

    start_date = date(year, 1, 1)
    if year == 2018:
        end_date = date.today() + timedelta(days=1)
    else:
        end_date = date(year+1, 1, 1)

    result = pd.DataFrame()

    for day in daterange(start_date, end_date):
        path = os.path.abspath(os.path.join(PATH.format(year), 'rezultatePZU_{}_{}_{}.csv'.format(day.month, day.day, year)))
        print(path)

        content = pd.read_csv(path, 
                          delimiter=',', 
                          header=None, 
                          skiprows=9,
                          names=HEADERS)

        result = result.append(content)
    result = result.drop(columns=['Trading_Zone', 'Interval'])
    result.to_csv(os.path.abspath(os.path.join(BASE_PATH,'opcom_{}.csv'.format(year))), encoding='utf-8', index=False)

get_old_data()

for year in range(2015, 2019):
    transform_data(year)
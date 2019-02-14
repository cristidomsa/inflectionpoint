from bs4 import BeautifulSoup
from datetime import datetime

import requests
import pandas as pd

MAP = {'HU': 'hungary',
        'CZ': 'czech_republic',
        'SK': 'slovakia',
        'GER': 'germany',
        'RO': 'romania'}

URL = "http://www.officeholidays.com/countries/{}/{}.php"

def get_country(country, year):
    holidays = []
    page = requests.get(URL.format(MAP[country], year))

    soup = BeautifulSoup(page.content, 'html.parser')

    entries = soup.find_all('tr', class_='holiday')

    for entry in entries:
        cells = entry.findAll('td')
        if country == 'CZ':
            try:
                text = cells[1].text.strip()
                date = datetime.strptime(text, "%B %d").replace(year=year)
                holidays.append(date.strftime("%Y-%m-%d"))
            except Exception as e:
                print('Error parsing holiday date in {} for country {}'.format(year, country))
        else:
            holidays.append(cells[1].find(datetime=True).string)
    
    return holidays

def get_holidays():

    result = {}

    for country in MAP.keys():
        holidays = []
        for year in range(2015, 2019):
            holidays.append(get_country(country, year))
        
        result[country] = sum(holidays, [])

    return result
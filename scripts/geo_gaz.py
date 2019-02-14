import pandas as pd
from geopy import geocoders

HEADERS = ['Name', 'Latitude', 'Longitude', 'Consum', 'Judet', 'Regiune']
UNK = {'CHENDU VALEA NIRAJULUI': 'VALEA NIRAJULUI',
       'SC RUBIN KING CAREI': 'CAREI',
        'UNGHENI-VALEA MURESULUI': 'UNGHENI',
        'GOVORA (RAURENI)': 'RAURENI',
        'BOD MENAJ': 'BOD',
        'GALDA DE JOS TEIUS': 'GALDA DE JOS',
        'UM MIERCUREA CIUC': 'MIERCUREA CIUC',
        'CABANA CHEIA RASNOV': 'RASNOV',
        'MATCA (VEGA 93)': 'MATCA',
        'LANCRAM II': 'LANCRAM',
        'SANATORIU PREDEAL': 'PREDEAL',
        'HUNEDOARA II': 'HUNEDOARA',
        'SAULIA (DE CAMPIE)': 'SAULIA',
        #'CORUNCA INMAGAZINAT': 'CORUNCA',
        #'ROMGAZ INMAGAZINAT': 'PLOIESTI'
        }

REGIUNI = {'Cluj': ['CJ', 'BN', 'MS'],
           'Vest': ['TM', 'AR', 'BH'],
           'Baia Mare': ['MM', 'SM', 'SJ'],
           'Centru': ['HD', 'AB', 'SB'],
           'Brasov': ['BV', 'CV', 'HR'],
           'Moldova Nord': ['SV', 'BT', 'NT', 'IS'],
           'Moldova Sud': ['BC', 'VS', 'VN'],
           'Baragan': ['GL', 'TL', 'BZ', 'BR'],
           'Dobrogea': ['CT', 'CL', 'IL'],
           'Bucuresti': ['B', 'IF', 'GR', 'TR'],
           'Muntenia': ['PH', 'AG', 'DB'],
           'Sud': ['GJ', 'VL'],
           'Oltenia': ['OT', 'MH', 'DJ', 'CS']
}

geo = geocoders.GeoNames(username='cristi.domsa')

df = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/gaz/alocari.csv')

locations = []

def get_region(county):
    for cnt in REGIUNI.keys():
        if county in REGIUNI[cnt]:
            return cnt
    
    return 'None'

def get_geo(names):
    for loc in names:
        point = []
        info = geo.geocode(loc + ', Romania')
        if not info:
            info = geo.geocode(UNK[loc] + ', Romania')

        if info:
            point.append(loc)
            point.append('+{}'.format(info.latitude))
            point.append('+{}'.format(info.longitude))
            point.append(str(df.loc[df['denumire Punct Virtual'] == loc, 'alocare finala'].sum()))
            try:
                county = info.raw['adminCodes1']['ISO3166_2']
                point.append(county)
                point.append(get_region(county))
            except Exception as e:
                print('Judet pentru: {} - Error'.format(loc))
                point.append('None')
                point.append('None')
            
            locations.append(point)
        
        else:
            print('Location: {} - UNK'.format(loc))

get_geo(set(df['denumire Punct Virtual']))

with open('/media/cristi/DATA/projects/inflectionPoint/geo/locations_jud.csv', 'w') as f:
    f.write(','.join(HEADERS) + '\n')
    for s in locations:
        f.write(','.join(s) + '\n')
    
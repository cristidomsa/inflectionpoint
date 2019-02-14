import pandas as pd

REGIUNI =['Cluj', 'Vest', 'Baia Mare', 'Centru', 'Brasov', 'Moldova Nord', 'Moldova Sud', 'Baragan',
            'Dobrogea', 'Bucuresti', 'Muntenia', 'Sud', 'Oltenia']

REGIUNI_IST = {'Transilvania', 'Banat', 'Crisana', 'Maramures', 'Bucovina', 'Moldova', 'Muntenia', 'Dobrogea', 'Oltenia'
}

MAPP = {'COVI CONSTRUCT 2000': ['B'],
        'CAMPULUNG MOLDOVENESC': ['SV'],
        'CPL CONCORDIA': ['CJ', 'SJ', 'SM'],
        'DELGAZ GRID': ['CJ', 'MS', 'SB'],
        'DISTRIGAZ SUD RETELE': ['B'],
        'GAZ NORD EST': ['SV'],
        'GAZMIR': ['IS'],
        'MACIN': ['BR'],
        'PREMIER ENERGY': ['B'],
        'RADAUTI': ['SV'],
        'SC RUBIN KING CAREI': ['BH'],
        'TEHNOLOGICA RADION': ['AG'],
        'TIMGAZ': ['TM'],
        'TULCEA': ['TL'],
        }

def get_gaz_data():
    dateparse = lambda x: pd.datetime.strptime(x, '%d.%m.%Y')

    nova_data = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/gaz/alocari_nov.csv', 
                            usecols=[2,4,6],
                            skip_blank_lines=True,
                            skiprows=4,
                            parse_dates=['zi consum'], 
                            date_parser=dateparse,
                            header=0)
    
    return nova_data.rename(columns=lambda x: x.strip())

def get_locations_regions():
    locations_regions = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/geo/locations_jud.csv', usecols=['Name', 'Regiune'], header=0)

    return locations_regions
    
def get_region_station_ids(region):

    stations = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/geo/stations_8.csv')

    return [int(station[0]) for station in stations[stations['Regiune'] == region].values]

def get_temp_for_list(cnt_list):

    stations = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/geo/stations_8.csv')
    return [int(station[0]) for station in stations[stations['Judet'].isin(cnt_list)].values]

if __name__ == "__main__":

    data_nova = get_gaz_data()
    #data_nova.groupby('Den_PV').groups().keys().tolist()

    # print(data_nova.groupby('Den_PV').groups.keys())

    # with open('locatii.csv', 'w') as f:
    #     import csv
    #     writer = csv.writer(f)
    #     writer.writerow(['Partener', 'Locatie'])
    #     for k in data_nova.groupby('Den_PV').groups.keys():
    #         writer.writerow([k])

    # data_loc_reg = get_locations_regions()
    # data_loc_reg.columns=['Den_PV', 'Regiune']
    # cols = 'Den_PV'
    # data_nova = data_nova.join(data_loc_reg.set_index(cols), on=cols)

    # data_nova.rename(columns={'Zi': 'Date'}, inplace=True)

    filename = r'/media/cristi/DATA/projects/inflectionPoint/weather/temperature_latest.csv'

    data_temp = pd.DataFrame()

    data = pd.read_csv(filename, parse_dates=['Date'], skiprows=1, header=None, names=['Station', 'Date', 'Time', 'Temp', 'Temp_Q'])

    df = data[data['Temp_Q'] == 1].groupby(['Station', 'Date'])['Temp'].mean().to_frame().reset_index()

    #df.to_csv('temp_reg.csv')
    # = get_temp_for_list(MAPP['CPL CONCORDIA'])

    #data_nova['Temp'] = df[df['Station'].isin(get_temp_for_list(MAPP[data_nova['Den_PV']]))]
    temps = pd.DataFrame()
    for pv in MAPP.keys():
        stations_list = get_temp_for_list(MAPP[pv])
        
        agg = df[df['Station'].isin(stations_list)].groupby('Date')['Temp'].mean().to_frame().reset_index()
        agg['Den_PV'] = pv

        temps = temps.append(agg)

    data_nova.rename(columns={'Zi':'Date'}, inplace=True)
    temps.to_csv('temps_nou.csv', index=False)
    data_nova.merge(temps, on=['Date', 'Den_PV']).to_csv('gaz_nou.csv', index=False)

    quit()
    cols = ['Date', 'Regiune']
    data_nova = data_nova.join(data_temp.set_index(cols), on=cols)

    data_nova_reg = data_nova.groupby(['Date', 'Regiune'])['alocare finala'].sum().to_frame().reset_index()

    data_nova_reg = data_nova_reg.join(data_temp.set_index(cols), on=cols)

    data_nova_reg.to_csv('../gaz/nova_data_reg.csv', index=False)
    #data_nova.to_csv('../gaz/nova_data.csv')

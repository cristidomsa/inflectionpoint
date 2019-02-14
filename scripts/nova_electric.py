import pandas as pd

REGIUNI =['Cluj', 'Vest', 'Baia Mare', 'Centru', 'Brasov', 'Moldova Nord', 'Moldova Sud', 'Baragan',
            'Dobrogea', 'Bucuresti', 'Muntenia', 'Sud', 'Oltenia']

REGIUNI_IST = {'Transilvania': ['CJ', 'BN', 'MS', 'HD', 'AB', 'SB', 'BV', 'CV', 'HR', 'SJ'],
           'Banat': ['TM', 'CS'],
           'Crisana': ['BH', 'AR'],
           'Maramures': ['MM', 'SM', ],
           'Bucovina': ['SV', 'BT'],
           'Moldova': ['BC', 'VS', 'VN', 'NT', 'IS', 'GL'],
           'Muntenia': ['PH', 'AG', 'DB', 'B', 'IF', 'GR', 'TR', 'IL', 'BZ', 'BR', 'CL',],
           'Dobrogea': ['CT',  'TL'],
           'Oltenia': ['OT', 'MH', 'DJ', 'GJ', 'VL']
}

WIND = ['Baragan','Dobrogea']
WIND_SEC = ['CS', 'GL', 'TL', 'CT', 'IL']

def convert_time(time):
    formatted = str(time).zfill(4)
    return formatted[:2] + ':' + formatted[2:]


def get_electric_data():
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

    nova_data = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/data/data_15-18_price_zeroed.csv', 
                            parse_dates=['Date'], 
                            date_parser=dateparse,
                            header=0)

    return nova_data

def get_locations_regions():
    locations_regions = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/geo/locations_jud.csv', usecols=['Name', 'Regiune'], header=0)

    return locations_regions
    
def get_region_station_ids(region, field='Regiune'):

    stations = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/geo/stations.csv')

    return [int(station[0]) for station in stations[stations[field] == region].values]

def get_wind_data():
    filename = r'/media/cristi/DATA/projects/inflectionPoint/weather/wind.csv'

    df = pd.read_csv(filename, parse_dates=['Date'], skiprows=1, header=None, names=['Station', 'Date', 'Time', 'Wind', 'Wind_Q'])

    df = df[df['Wind_Q'] == 1].groupby(['Station', 'Date'])['Wind'].mean().to_frame().reset_index()

    #df['Time'] = convert_time(df["Time"])

    # del df["Date"], df["Time"]
    # df.rename({'DateTime': 'Date'})

    return df

if __name__ == "__main__":

    data_electric = get_electric_data()
    data_loc_reg = get_locations_regions()

    data_wind = get_wind_data()

    data = pd.DataFrame()
    #df.to_csv('temp_reg.csv')
    
    for region in WIND_SEC:
        stations_list = get_region_station_ids(region, field='Judet')
        
        agg = data_wind[data_wind['Station'].isin(stations_list)].groupby(['Date'])['Wind'].mean().to_frame().reset_index()

        if data.empty:
            data = agg
            data.rename(columns={'Wind': region}, inplace=True)
        else:
            data[region] = agg['Wind']

    data.to_csv('wind_judete.csv', index=False)
    
    # data_electric = data_electric.join(data_wind.set_index(cols), on=cols)
    #data_electric.to_csv('../data/nova_electric.csv')

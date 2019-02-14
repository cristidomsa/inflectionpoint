import pandas as pd
from os import path

base_path = '/media/cristi/DATA/projects/inflectionPoint/entsoe/prod'
filename = 'Actual Generation per Production Type_{}01010000-{}01010000.csv'
header_cols = ['Date', 'Biomasa', 'Carbune_1', 'Hidrocarburi', 'Carbune_2', 'Ape_curg', 'Ape_Bazin', 'Nuclear', 'Solar', 'Eolian']
cols = ['Biomasa', 'Carbune', 'Hidrocarburi', 'Ape_curg', 'Ape_Bazin', 'Nuclear', 'Solar', 'Eolian']

def get_historic_data(year):
    df = pd.read_csv(path.join(base_path, filename.format(year, year+1)), 
                     usecols=[1,2,3,5,6,13,14,16,19,22], 
                     header=None,
                     skiprows=1,
                     parse_dates=['Date'],
                     names=header_cols,
                     index_col='Date',
                     date_parser=lambda x: pd.datetime.strptime(x.split(' - ')[0], '%d.%m.%Y %H:%M')
    ).dropna()

    df = df.apply(pd.to_numeric, errors='coerce')
    # df['Carbune_1'] = df['Carbune_1'].apply(pd.to_numeric, errors='coerce')
    # df['Carbune_2'] = df['Carbune_2'].apply(pd.to_numeric, errors='coerce')

    df['Carbune'] = df['Carbune_1'] + df['Carbune_2']
    df.drop(columns=['Carbune_1', 'Carbune_2'], inplace=True)
    
    return df

if __name__ == '__main__':

    df = pd.DataFrame()
    for year in range(2015, 2019):
        df = df.append(get_historic_data(year))
        
    df.dropna().to_csv(path.join(base_path, 'prod_entsoe.csv'))
    df.resample('1D').agg({k: 'mean' for k in cols[1:]}).dropna().to_csv(path.join(base_path, 'prod_entsoe_banda.csv'))
    df.between_time('07:00', '21:00').resample('1D').agg({k: 'mean' for k in cols[1:]}).dropna().to_csv(path.join(base_path, 'prod_entsoe_peak.csv'))
    df.between_time('21:00', '07:00').resample('1D').agg({k: 'mean' for k in cols[1:]}).dropna().to_csv(path.join(base_path, 'prod_entsoe_off_peak.csv'))
import pandas as pd

COLS_PRICES = ['Price_RO', 'Price_HU', 'Price_SK', 'Price_CZ', 'Price_GER', 'Price_FR']
COLS_PRICES_EXT = ['Price_HU', 'Price_SK', 'Price_CZ', 'Price_GER', 'Price_FR']
COLS_PROD = ['Prod_total','Prod_Carbune','Prod_Hidrocarburi','Prod_Ape','Prod_Nuclear','Prod_Eolian','Prod_Foto','Prod_Biomasa','Sold']
COLS_ENT_PROD = ['Biomasa', 'Carbune_1', 'Hidrocarburi', 'Carbune_2', 'Ape_curg', 'Ape_Bazin', 'Nuclear', 'Solar', 'Eolian']
COLS_RO = ['Price_RO']

ALL_DATA_FILENAME = '/media/cristi/DATA/projects/inflectionPoint/data/data_15-18_price_normal.csv'
NOV_DATA = '/media/cristi/DATA/projects/inflectionPoint/data/trans_all.csv'
NOV_PRICE_DATA = '/media/cristi/DATA/projects/inflectionPoint/entsoe/price_2018.csv'
ENT_PROD_DATA = '/media/cristi/DATA/projects/inflectionPoint/entsoe/prod/prod_entsoe.csv'

TYPES = ['max', 'mean']

def get_electric_data(file=NOV_PRICE_DATA):
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

    nova_data = pd.read_csv(file, 
                            parse_dates=['Date'], 
                            date_parser=dateparse,
                            index_col='Date',
                            header=0)

    return nova_data

def make_zero_prices(df, cols=COLS_PROD):
    for col in cols:
        df.loc[df[col] < 0, col] = 0
    return df

def make_price_files(df, cols=COLS_PROD):
    for op in TYPES:

        df.between_time('07:00', '22:00').resample('1D').agg({k: op for k in cols}).dropna().to_csv('ro_{}_peak_ext.csv'.format(op))

        df.between_time('22:00', '07:00').resample('1D').agg({k: op for k in cols}).dropna().to_csv('ro_{}_off_peak_ext.csv'.format(op))

        df.resample('1D').agg({k: op for k in cols}).dropna().to_csv('ro_{}_base_ext.csv'.format(op))        

if __name__ == "__main__":

    on_cols = COLS_RO
    df = get_electric_data()
    df = make_zero_prices(df, cols=on_cols)
    make_price_files(df, cols=on_cols)

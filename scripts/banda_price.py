import pandas as pd

COLS_PRICES = ['Price_RO', 'Price_HU', 'Price_SK', 'Price_CZ', 'Price_GER', 'Price_FR']
COLS_PRICES_EXT = ['Price_HU', 'Price_SK', 'Price_CZ', 'Price_GER', 'Price_FR']

ALL_DATA_FILENAME = '/media/cristi/DATA/projects/inflectionPoint/data/data_15-18_price_normal.csv'
NOV_DATA = '/media/cristi/DATA/projects/inflectionPoint/scripts/price_2018.csv'

TYPES = ['max', 'mean']

def get_electric_data():
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

    nova_data = pd.read_csv(NOV_DATA, 
                            parse_dates=['Date'], 
                            date_parser=dateparse,
                            index_col='Date',
                            header=0)

    return nova_data

def make_zero_prices(df):
    for col in COLS_PRICES[0]:
        df.loc[df[col] < 0, col] = 0
    return df

def make_price_files(df):
    for op in TYPES:

        df.between_time('07:00', '22:00').resample('1D').agg({
                                #'Price_RO': op,
                                'Price_HU': op,
                                'Price_SK': op,
                                'Price_CZ': op,
                                'Price_GER': op,
                                'Price_FR': op, 
        }).dropna().to_csv('pret_{}_peak_ext.csv'.format(op))

        df.between_time('22:00', '07:00').resample('1D').agg({
                                #'Price_RO': op,
                                'Price_HU': op,
                                'Price_SK': op,
                                'Price_CZ': op,
                                'Price_GER': op,
                                'Price_FR': op, 
        }).dropna().to_csv('pret_{}_off_peak_ext.csv'.format(op))

        df.resample('1D').agg({
                                #'Price_RO': op,
                                'Price_HU': op,
                                'Price_SK': op,
                                'Price_CZ': op,
                                'Price_GER': op,
                                'Price_FR': op, 
        }).dropna().to_csv('pret_{}_base_ext.csv'.format(op))        

if __name__ == "__main__":

    df = get_electric_data()
    df = make_zero_prices(df)
    make_price_files(df)

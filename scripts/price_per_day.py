import pandas as pd

ALL_DATA_FILENAME = '/media/cristi/DATA/projects/inflectionPoint/data/data_15-18_price_normal.csv'
NOV_DATA = '/media/cristi/DATA/projects/inflectionPoint/scripts/price_nov.csv'

def get_electric_data():
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

    nova_data = pd.read_csv(NOV_DATA, 
                            parse_dates=['Date'], 
                            date_parser=dateparse,
                            index_col='Date',
                            header=0)

    return nova_data


if __name__ == "__main__":

    df = get_electric_data()
    df.resample('1D').agg({
                           'Price_RO': 'sum',
                           'Price_HU': 'sum',
                           'Price_SK': 'sum',
                           'Price_CZ': 'sum',
                           'Price_GER': 'sum',
                           'Price_FR': 'sum', 
    }).dropna().to_csv('pret_sum.csv')
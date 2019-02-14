import pandas as pd

#HEADER = ['Date','Price_CZ','Price_HU','Price_SK','Price_FR','Price_GER','Price_RO','Traded_RO','Traded_RO_buy','Traded_RO_sell','RO_HU','HU_RO','HU_SK','SK_HU','SK_CZ','CZ_SK','Holiday_HU','Holiday_CZ','Holiday_SK','Holiday_GER','Holiday_RO','Quarter','Weekend','Consum','Prod_total','Prod_Carbune',Prod_Hidrocarburi,Prod_Ape,Prod_Nuclear,Prod_Eolian,Prod_Foto,Prod_Biomasa,Sold]

df = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/transelectrica/consum_2015_2018.csv', skiprows=2, header=0, parse_dates=[0], date_parser=lambda x: pd.datetime.strptime(x, '%d.%m.%Y'))


df.set_index('Date', inplace=True)

get_max = lambda x: x.value_counts(dropna=False).index[0]
get_max.__name__ = "most frequent"

df = df.resample('1D').agg({'Consum': 'mean',
                            'Weekend': get_max,
                            'Holiday_RO': get_max,
                            }).dropna()

df_temp = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/scripts/temp_all.csv', parse_dates=['Date'], header=0)

cols = ['Date']

df.join(df_temp.set_index(cols), on=cols).dropna().to_csv('electric_consum_temp.csv')
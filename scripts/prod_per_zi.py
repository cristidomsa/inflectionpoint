import pandas as pd

#HEADER = ['Date','Price_CZ','Price_HU','Price_SK','Price_FR','Price_GER','Price_RO','Traded_RO','Traded_RO_buy','Traded_RO_sell','RO_HU','HU_RO','HU_SK','SK_HU','SK_CZ','CZ_SK','Holiday_HU','Holiday_CZ','Holiday_SK','Holiday_GER','Holiday_RO','Quarter','Weekend','Consum','Prod_total','Prod_Carbune',Prod_Hidrocarburi,Prod_Ape,Prod_Nuclear,Prod_Eolian,Prod_Foto,Prod_Biomasa,Sold]

df = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/data/data_15-18_price_normal.csv', parse_dates=['Date'], header=0, usecols=['Date', 'Prod_Eolian'])

df.set_index('Date', inplace=True)

df = df.resample('1D').agg({'Prod_Eolian': 'mean'}).dropna()

df_temp = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/scripts/wind_judete.csv', parse_dates=['Date'], header=0)

cols = ['Date']

df.join(df_temp.set_index(cols), on=cols).dropna().to_csv('electric_prod_vant.csv')
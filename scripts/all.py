import pandas as pd

cols = ['Price_FR','Price_GER','Price_RO','Price_HU','Price_SK','Price_CZ','RO_HU','HU_RO','HU_SK','SK_HU','SK_CZ','CZ_SK','Traded_RO','Traded_RO_buy','Traded_RO_sell','Biomasa','Hidrocarburi','Ape_curg','Ape_Bazin','Nuclear','Solar','Eolian','Carbune','Consum']

cols_max = ['Holiday_HU','Holiday_CZ','Holiday_SK','Holiday_GER','Holiday_RO','Quarter','Weekend']

prod = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/data/prod_entsoe.csv', index_col=0, parse_dates=[0], header=0)

price = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/data/prices.csv', index_col=0, parse_dates=[0], header=0)

consum = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/data/consum.csv', index_col=0, parse_dates=[0], header=0)

get_max = lambda x: x.mode()
get_max.__name__ = "most frequent"

agg_dict = {k: 'mean' for k in cols}
max_dict = {k: get_max for k in cols_max}

agg_dict.update(max_dict)

df = price.merge(prod, on='Date').merge(consum, on='Date')

df.to_csv('../data/data.csv')

df.resample('1D').agg(agg_dict).dropna().to_csv('../data/data_banda.csv')
df.between_time('07:00', '21:00').resample('1D').agg(agg_dict).dropna().to_csv('../data/data_peak.csv')
df.between_time('21:00', '07:00').resample('1D').agg(agg_dict).dropna().to_csv('../data/data_off_peak.csv')
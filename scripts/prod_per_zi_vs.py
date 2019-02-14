import pandas as pd

df = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/data/data_15-18_price_normal.csv', index_col='Date', parse_dates=['Date'], header=0, usecols=['Date', 'Prod_total', 'Prod_Carbune', 'Prod_Hidrocarburi', 'Prod_Ape', 'Prod_Nuclear', 'Prod_Eolian', 'Prod_Foto','Prod_Biomasa'])


df = df.resample('1D').agg({'Prod_total': 'sum',
                       'Prod_Carbune': 'sum',
                       'Prod_Hidrocarburi': 'sum',
                       'Prod_Ape': 'sum', 
                       'Prod_Nuclear': 'sum', 
                       'Prod_Eolian': 'sum', 
                       'Prod_Foto': 'sum',
                       'Prod_Biomasa': 'sum'})

df['Prod_Conv'] = df['Prod_Carbune'] + df['Prod_Hidrocarburi'] + df['Prod_Nuclear']
df['Prod_Verde'] = df['Prod_Ape'] + df['Prod_Eolian'] + df['Prod_Foto'] + df['Prod_Biomasa']

df.to_csv('prod_per_zi.csv')
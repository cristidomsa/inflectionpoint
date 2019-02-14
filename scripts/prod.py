import pandas as pd

df = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/scripts/transelectrica_nov.csv')

df.loc[df['Prod_Eolian'] < 0, 'Consum']= df['Consum'] - df['Prod_Eolian']
df.loc[df['Prod_Foto'] < 0, 'Consum'] = df['Consum'] - df['Prod_Foto']

df['Prod_Eolian'][df['Prod_Eolian'] < 0] = 0
df['Prod_Foto'][df['Prod_Foto'] < 0] = 0

COL_LIST = ['Prod_Carbune','Prod_Hidrocarburi','Prod_Ape','Prod_Nuclear','Prod_Eolian','Prod_Foto','Prod_Biomasa']

df['Prod_total'] = df[COL_LIST].sum(axis=1)
df['Sold'] = df['Consum'] - df['Prod_total']

df.to_csv('trans_data.csv', index=False)
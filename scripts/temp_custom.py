import pandas as pd

df = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/weather/temp_latest_dec.csv', parse_dates=[2], index_col=2)

df.drop(columns=['Unnamed: 0'], inplace=True)

df.loc[df['Station'] == 150850].to_csv('temp_bistrita.csv')

df.loc[df['Station'] == 152600].to_csv('temp_copsa_mica.csv')
import pandas as pd

df_temp_old = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/scripts/temp_regiuni.csv', parse_dates=['Date'], header=0)
df_temp_new = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/scripts/temp_latest_regiuni.csv', parse_dates=['Date'], header=0)

pd.concat([df_temp_old, df_temp_new], ignore_index=False, sort=True).set_index('Date').to_csv('temp_all.csv')
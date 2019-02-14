import pandas as pd

df_prod = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/entsoe/prod/prod_entsoe.csv', parse_dates=[0], index_col=[0])

df_price = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/scripts/prices_hu_ro_zi.csv', parse_dates=[0], index_col=[0])

df_consum = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/transelectrica/consum.csv', 
                        parse_dates=[0], 
                        index_col=[0],
                        date_parser=lambda x: pd.datetime.strptime(x, '%d.%m.%Y'))

df_temp = pd.read_csv('/media/cristi/DATA/projects/inflectionPoint/scripts/temp_all.csv',
                        parse_dates=[0],
                        index_col=[0],
                        date_parser=lambda x: pd.datetime.strptime(x, '%Y-%m-%d'))

df_temp['Temp_medie'] = (df_temp['Banat'] + 
                    df_temp['Bucovina'] + 
                    df_temp['Crisana'] + 
                    df_temp['Dobrogea'] + 
                    df_temp['Maramures'] +
                    df_temp['Moldova'] +
                    df_temp['Muntenia'] +
                    df_temp['Oltenia'] +
                    df_temp['Transilvania']) / 9

df_temp.drop(columns=['Banat','Bucovina','Crisana','Dobrogea','Maramures','Moldova','Muntenia','Oltenia','Transilvania'], inplace=True)

df_prod.join(df_price).join(df_consum).join(df_temp).to_csv('date.csv')


import pandas as pd

filename = r'/media/cristi/DATA/projects/inflectionPoint/weather/9685427807234dat.txt'

pd.read_csv(filename, usecols=[0,2,3,7,8], skiprows=2, header=None).to_csv('../weather/temperature_latest.csv', index=False)


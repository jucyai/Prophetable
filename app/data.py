import pandas as pd

from common import read_config


config = read_config('data/config.json')
print(config)

df = pd.read_csv('data/example.csv')
print(df.head())

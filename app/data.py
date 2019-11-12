import pandas as pd

from common import read_config


config = read_config('data/config.json')

datafile = config.get('datafile') or 'example.csv'
delimiter = config.get('delimiter') or ','
ds_col = config.get('ds') or 'ds'
y_col = config.get('y') or 'y'
ts_freq = config.get('tsfreq') or 'D'
max_train_date = config.get('maxtraindate')
min_train_date = config.get('mintraindate')
na_fill = float(config.get('nafill') or 0)
holidays = config.get('holidays')

data = pd.read_csv('data/'+datafile, sep=delimiter)

if max_train_date is None:
    max_train_date = data[ds_col].max()
if min_train_date is None:
    min_train_date = data[ds_col].min()

model_data = pd.DataFrame(
    {'ds': pd.date_range(min_train_date, max_train_date, freq=ts_freq)}
)
data[ds_col] = pd.to_datetime(data[ds_col], infer_datetime_format=True)
model_data = model_data.merge(data[[ds_col, y_col]], left_on='ds', right_on=ds_col, how='left')
model_data = model_data.drop(columns=[ds_col])
model_data = model_data.rename(columns={y_col: 'y'})
model_data = model_data.fillna(na_fill)

holidays_data = None
if holidays is not None:
    for i, h in enumerate(holidays):
        holidays[i]['ds'] = pd.to_datetime(h['ds'])
        holidays[i] = pd.DataFrame(holidays[i])
    holidays_data = pd.concat(holidays)

model_data.to_csv('data/model_data.csv', index=False)
holidays_data.to_csv('data/holidays_data.csv', index=False)

import pandas as pd

from common import read_config


config = read_config('data/config.json')
data = pd.read_csv('data/example.csv')

ds_col = config.get('ds') or 'ds'
y_col = config.get('') or 'y'
ts_freq = config.get('ts_freq') or 'D'
na_fill = float(config.get('na_fill') or 0)
holidays = config.get('holidays')

model_data = pd.DataFrame(
    {'ds': pd.date_range(data[ds_col].min(), data[ds_col].max(), freq=ts_freq)}
)
data[ds_col] = pd.to_datetime(data[ds_col], infer_datetime_format=True)
model_data = model_data.merge(data[[ds_col, y_col]], left_on='ds', right_on=ds_col, how='left')

model_data = model_data.fillna(na_fill)

holidays_data = None
if holidays is not None:
    for i, h in enumerate(holidays):
        holidays[i]['ds'] = pd.to_datetime(h['ds'])
        holidays[i] = pd.DataFrame(holidays[i])
    holidays_data = pd.concat(holidays)

model_data.to_csv('data/model_data.csv', index=False)
holidays_data.to_csv('data/holidays_data.csv', index=False)

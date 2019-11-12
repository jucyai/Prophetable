import pandas as pd
from fbprophet import Prophet

from common import read_config


config = read_config('data/config.json')
ts_freq = config.get('tsfreq') or 'D'
future_periods = config.get('futureperiods') or 10
floor = config.get('floor')

train_data = pd.read_csv('data/model_data.csv')

holidays_data = None
if config.get('holidays') is not None:
    holidays_data = pd.read_csv('data/holidays_data.csv')

if floor is not None:
    train_data['floor'] = floor

model = Prophet(
    # changepoint_prior_scale=0.05,
    yearly_seasonality=True,
    holidays=holidays_data
    # holidays_prior_scale=5
)
model.fit(train_data)
df_future = model.make_future_dataframe(
    periods=future_periods,
    freq=ts_freq
)
forecast = model.predict(df_future)

forecast.to_csv('data/output.csv', index=False)

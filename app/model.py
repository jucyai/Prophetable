import pandas as pd
from fbprophet import Prophet

df = pd.read_csv('data/example.csv')

model = Prophet()
model.fit(df)
df_future = model.make_future_dataframe(periods=365)
df_future.tail()
forecast = model.predict(df_future)

forecast.to_csv('data/output.csv', index=False)

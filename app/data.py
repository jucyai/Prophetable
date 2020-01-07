from prophet import Data


d = Data(config='data/config.json')
d.make_model_data('data/model_data.csv')
d.make_holidays_data('data/holidays_data.csv')

from prophet import Data


d = Data(config='data/prophet-config.json')
d.make_model_data()
d.make_holidays_data()

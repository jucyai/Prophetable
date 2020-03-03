from prophetable import Prophetable

p = Prophetable(config='data/config.full.json')
p.make_data()
p.train()
p.predict()
print(p.forecast.tail())

from prophetable import Prophetable

p = Prophetable(config='data/config.minimal.json')
p.make_data()
p.train()
p.predict()
print(p.forecast.tail())

from prophetable import Prophetable

# p = Prophetable(config='data/config.full.json')
p = Prophetable(config='data/config.seasonalities.json')
p.run()
print(p.forecast.tail())

try:
    print(p.model.seasonalities)
except:
    print('No seasonalities')

try:
    print(p.model.train_holiday_names)
except:
    print('No built-in holidays')

try:
    print(
        p.forecast[
            (p.forecast['playoff'] + p.forecast['superbowl']).abs() > 0
        ][['ds', 'playoff', 'superbowl']][-10:]
    )
except:
    print('No custom holidays')

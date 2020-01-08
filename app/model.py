from prophet import Model


m = Model(config='data/prophet-config.json')
m.train()
m.predict()
m.save_model()
m.load_model(overwrite=True)

from core import Model


m = Model(config='data/config.json')
m.train(
    train_data_file='data/model_data.csv',
    outfile='data/output.csv',
    holidays_data_file='data/holidays_data.csv'
)

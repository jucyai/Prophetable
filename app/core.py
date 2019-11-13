import json

import pandas as pd
from fbprophet import Prophet


def _read_config(filename):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config


class Common:
    """Base class
    """
    def __init__(self, config):
        config = _read_config(config)
        self.datafile = config.get('datafile') or 'example.csv'
        self.delimiter = config.get('delimiter') or ','
        self.floor = config.get('floor')
        self.ds_col = config.get('ds') or 'ds'
        self.y_col = config.get('y') or 'y'
        self.ts_freq = config.get('tsfreq') or 'D'
        self.max_train_date = config.get('maxtraindate')
        self.min_train_date = config.get('mintraindate')
        self.na_fill = float(config.get('nafill') or 0)
        self.future_periods = config.get('futureperiods')
        self.holidays = config.get('holidays')
        self.data = pd.read_csv('data/'+self.datafile, sep=self.delimiter)
        if self.max_train_date is None:
            self.max_train_date = self.data[self.ds_col].max()
        if self.min_train_date is None:
            self.min_train_date = self.data[self.ds_col].min()


class Data(Common):
    """Data processing
    """
    def __init__(self, config):
        super().__init__(config=config)
    
    def make_model_data(self, outfile):
        model_data = pd.DataFrame(
            {'ds': pd.date_range(self.min_train_date, self.max_train_date, freq=self.ts_freq)}
        )
        data_copy = self.data.copy()
        data_copy[self.ds_col] = pd.to_datetime(data_copy[self.ds_col], infer_datetime_format=True)
        model_data = model_data.merge(
            data_copy[[self.ds_col, self.y_col]], left_on='ds', right_on=self.ds_col, how='left'
        )
        if self.ds_col != 'ds':
            model_data = model_data.drop(columns=[self.ds_col])
        model_data = model_data.rename(columns={self.y_col: 'y'})
        model_data = model_data.fillna(self.na_fill)
        model_data.to_csv(outfile, index=False)
        return model_data

    def make_holidays_data(self, outfile):
        holidays_data = None
        that_holidays = self.holidays
        if that_holidays is not None:
            for i, h in enumerate(that_holidays):
                that_holidays[i]['ds'] = pd.to_datetime(h['ds'])
                that_holidays[i] = pd.DataFrame(that_holidays[i])
            holidays_data = pd.concat(that_holidays)
        holidays_data.to_csv(outfile, index=False)
        return holidays_data


class Model(Common):
    """Model training
    """
    def __init__(self, config):
        super().__init__(config=config)
    
    def train(self, train_data_file, outfile, holidays_data_file=None):
        train_data = pd.read_csv(train_data_file)

        holidays_data = None
        if  holidays_data_file is not None:
            holidays_data = pd.read_csv(holidays_data_file)

        if self.floor is not None:
            train_data['floor'] = self.floor
        
        model = Prophet(
            # changepoint_prior_scale=0.05,
            # holidays_prior_scale=5,
            yearly_seasonality=True,
            holidays=holidays_data
        ).fit(train_data)

        # TODO: separate to a predict method
        df_future = model.make_future_dataframe(
            periods=self.future_periods,
            freq=self.ts_freq
        )

        forecast = model.predict(df_future)
        forecast.to_csv(outfile, index=False)
        return forecast
import json

import pandas as pd
from fbprophet import Prophet


def _read_config(filename):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config


class Common:
    """Base class

    # Arguments:
        yearly_seasonality: Fit yearly seasonality. Can be 'auto', True, False, or a number of 
            Fourier terms to generate.
        weekly_seasonality: Fit weekly seasonality. Can be 'auto', True, False, or a number of 
            Fourier terms to generate.
        daily_seasonality: Fit daily seasonality.   Can be 'auto', True, False, or a number of 
            Fourier terms to generate.
    """
    def __init__(self, config):
        config = _read_config(config)
        self.datafile = config.get('datafile') or 'example.csv'
        self.train_datafile = config.get('traindatafile') or 'model_data.csv'
        self.model_output_file = config.get('modeloutputfile') # can be None
        self.model_pickle_file = config.get('modelpicklefile') # can be None
        self.holiday_datafile = config.get('holidaydatafile') # can be None
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
        self.yearly_seasonality = config.get('yearlyseasonality') or False
        self.weekly_seasonality = config.get('weeklyseasonality') or False
        self.daily_seasonality = config.get('dailyseasonality') or False
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
    
    def make_model_data(self, outfile=None):
        if outfile is None:
            outfile = self.train_datafile
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

    def make_holidays_data(self, outfile=None):
        if outfile is None:
            outfile = self.holiday_datafile
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
    """Model training and forecasting
    """
    def __init__(self, config):
        super().__init__(config=config)
        self.model = None
        self.forecast = None
    
    def train(self, train_data_file=None, holidays_data_file=None):
        if train_data_file is None:
            train_data_file = self.train_datafile
        train_data = pd.read_csv(train_data_file)

        holidays_data = None
        if  holidays_data_file is not None:
            holidays_data = pd.read_csv(holidays_data_file)
        elif self.holiday_datafile is not None:
            holidays_data = pd.read_csv(self.holiday_datafile)

        if self.floor is not None:
            train_data['floor'] = self.floor
        
        model = Prophet(
            yearly_seasonality=self.yearly_seasonality,
            weekly_seasonality=self.weekly_seasonality,
            daily_seasonality=self.daily_seasonality,
            holidays=holidays_data
        ).fit(train_data)

        self.model = model
        return model

    def predict(self, outfile=None):
        df_future = self.model.make_future_dataframe(
            periods=self.future_periods,
            freq=self.ts_freq
        )
        forecast = self.model.predict(df_future)
        self.forecast = forecast
        if outfile is None:
            outfile = self.model_output_file
        if outfile:
            forecast.to_csv(outfile, index=False)
        return forecast

    def save_model(self, filename=None):
        import pickle
        if filename is None:
            filename = self.model_pickle_file
        with open(filename, 'wb') as f:
            pickle.dump(self.model, f)

    def load_model(self, filename=None, overwrite=False):
        if filename is None:
            filename = self.model_pickle_file
        if self.model is not None and not overwrite:
            raise ValueError('Model already exists. Set overwrite to True to replace.')
        import pickle
        with open(filename, 'rb') as f:
            self.model = pickle.load(f)

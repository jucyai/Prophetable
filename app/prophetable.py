import json

import pandas as pd
from fbprophet import Prophet

import logging


log_format = 'Prophetable | %(asctime)s | %(name)s | %(levelname)s | %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_format)
logger = logging.getLogger(__name__)


class Prophetable:
    """Wrapping fbprophet.Prophet

    # Arguments:

        config: Config file URI
            # Prophetable config:
                # File related
                data_uri: URI for input data, required
                train_uri: URI for training data, if saving is needed
                output_uri: URI for forecast output, if saving is needed
                model_uri: URI for model object, if saving is needed
                holiday_uri: URI for holidays data, if provided
                delimiter: The delimiler for input data

                # Model related
                saturating_min: Maps to `floor` column in Prophet training data.
                saturating_max: Maps to `cap` column in Prophet training data.

            # Mapped directly from Prophet forecaster
                yearly_seasonality: Fit yearly seasonality. Can be 'auto', True, False, or a number
                    of Fourier terms to generate.
                weekly_seasonality: Fit weekly seasonality. Can be 'auto', True, False, or a number
                    of Fourier terms to generate.
                daily_seasonality: Fit daily seasonality.   Can be 'auto', True, False, or a number
                    of Fourier terms to generate.
    """
    def __init__(self, config):
        with open(config, 'r') as f:
            self._config = json.load(f)
        
        ## Required file uri
        for attr in ['data_uri']:
            self._get_config(attr)
        
        ## Nullable file uri
        # Intermedairy files will be stored in memory only
        for attr in [
            'train_uri',
            'output_uri',
            'model_uri',
            'holiday_uri'
        ]:
            self._get_config(attr, required=False)

        ## Other file related config
        self._get_config('delimiter', default=',', required=False)

        ## Model related config
        self._get_config('ds', default='ds', required=False)
        self._get_config('y', default='y', required=False)
        self._get_config('ts_frequency', default='D', required=False)
        # Modified in make_data()
        self._get_config('min_train_date', default=None, required=False) 
        # Modified in make_data()
        self._get_config('max_train_date', default=None, required=False)
        self._get_config('holidays', default=None, required=False)
        self._get_config('saturating_min', default=None, required=False, type_check=[int, float])
        self._get_config('saturating_max', default=None, required=False, type_check=[int, float])
        # Set the default na_fill to None
        # https://facebook.github.io/prophet/docs/outliers.html
        # Prophet has no problem with missing data. If you set their values to NA in the history but
        # leave the dates in future, then Prophet will give you a prediction for their values.
        self._get_config('na_fill', default=None, required=False, type_check=[int, float])

        ## Prediction
        self._get_config('future_periods', default=365, required=False, type_check=[int])

        ## Placeholder for other attributes set later
        self.data = None

    def _get_config(self, attr, required=True, default=None, type_check=None):
        try:
            set_attr = self._config[attr]
            if type_check is not None:
                if not any([isinstance(set_attr, t) for t in type_check]):
                    raise TypeError(f'{attr} provided is not {type_check}')
        except KeyError:
            if required:
                raise ValueError(f'{attr} must be provided in config')
            else:       
                set_attr = default
        setattr(self, attr, set_attr)
        logger.info(f'{attr} set to {set_attr}')

    def make_data(self):
        self.data = pd.read_csv(self.data_uri, sep=self.delimiter)
        self.data[self.ds] = pd.to_datetime(self.data[self.ds], infer_datetime_format=True)
        if self.min_train_date is None:
           self.min_train_date =  self.data[self.ds].min()
        if self.max_train_date is None:
           self.max_train_date =  self.data[self.ds].max()
        model_data = pd.DataFrame({
            'ds': pd.date_range(self.min_train_date, self.max_train_date, freq=self.ts_frequency)
        })
        model_data = model_data.merge(
            self.data[[self.ds, self.y]], left_on='ds', right_on=self.ds, how='left'
        )
        if self.ds != 'ds':
            model_data = model_data.drop(columns=[self.ds])
        model_data = model_data.rename(columns={self.y: 'y'})
        if self.na_fill is not None:
            model_data = model_data.fillna(self.na_fill)
        if self.saturating_min is not None:
            model_data['floor'] = self.saturating_min
        if self.saturating_max is not None:
            model_data['cap'] = self.saturating_max
        if self.train_uri is not None:
            model_data.to_csv(self.train_uri, index=False)
        self.data = model_data

    def train(self):
        """Method to train Prophet forecaster
        """
        model = Prophet().fit(self.data)
        self.model = model

    def predict(self):
        future = self.model.make_future_dataframe(
            periods=self.future_periods,
            freq=self.ts_frequency
        )
        forecast = self.model.predict(future)
        self.forecast = forecast
        if self.output_uri is not None:
            forecast.to_csv(self.output_uri, index=False)

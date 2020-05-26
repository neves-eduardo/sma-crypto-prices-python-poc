import pandas as pandas
import requests
import json

import plotly.graph_objs as graph_objs
from plotly.offline import plot

from pyti.smoothed_moving_average import smoothed_moving_average as sma


def collect_data(base, endpoint, symbol, time):
    params = '?&symbol='+symbol+'&interval=' + time
    data = requests.get(base + endpoint + params)
    dictionary = json.loads(data.text)

    dataframe = pandas.DataFrame.from_dict(dictionary)
    dataframe = dataframe.drop(range(6, 12), axis=1)

    dataframe.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
    for col in dataframe.columns:
        dataframe[col] = dataframe[col].astype(float)

    dataframe['fast_sma'] = sma(dataframe['close'].tolist(), 10)
    dataframe['slow_sma'] = sma(dataframe['close'].tolist(), 30)
    print(dataframe)

collect_data('https://api.binance.com', '/api/v1/klines', 'BTCUSDT', '1h')

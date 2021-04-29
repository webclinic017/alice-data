import datetime
import pandas as pd
import os
filename = str(datetime.datetime.now().date()) + ".txt"
loc = os.path.join(r"F:\Database\Alice-data\data", filename)
fh1 = open(loc, 'r')
data_txt = []


def get_data(symbol):
    a = fh1.readlines()
    for i in range(len(a)):
        a[i] = eval(a[i][:-1])
        a[i]['exchange_time_stamp'] = datetime.datetime.fromtimestamp(a[i]['exchange_time_stamp'])
    data_txt.extend(a)
    df = pd.DataFrame(data_txt)
    instruments = sorted(list(set(df['instrument'].values)))
    df2 = df[df.instrument == symbol].copy()
    df2.set_index('exchange_time_stamp', inplace=True)
    data = df2.ltp.resample('5Min').ohlc()
    data = data.rename({'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close'}, axis=1)
    return data


get_data("SBIN")
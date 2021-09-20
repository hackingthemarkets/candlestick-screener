import talib
import numpy as np
import yfinance as yf 
import os, pandas
import datetime
import time
from set_stock import *

class consolidating:

    start = "2021-01-01"
    # end = datetime.datetime.now()
    end = "2021-06-28"

    def is_consolidating(df, percentage=5):
        recent_candlesticks = df[-15:]

        max_close = recent_candlesticks['Close'].max()
        min_close = recent_candlesticks['Close'].min()
    

        threshold = 1 - (percentage / 100)
        if min_close > (max_close * threshold):
            return True        

        return False

    def get_price(df):
        current_close = df[-1:]
        price = current_close['Close'].values[0]

        return price

    def get_volume(df):
        current_volume = df[-1:]
        volume = current_volume['Volume'].values[0]

        return volume
    
    def get_volume_last5(df):
        df = df.tail(6)
        df = df.iloc[0:5]
        df = df['Volume']
        avg_vol5 = np.mean(df)
        return avg_vol5

      

    def is_breaking_out(df, percentage=2.5):
        last_close = df[-1:]['Close'].values[0]

        if is_consolidating(df[:-1], percentage=percentage):
            recent_closes = df[-16:-1]

            if last_close > recent_closes['Close'].max():
                return True

        return False

    data = []
    price_now = []
    volume = []
    increased_volume = []
    avg_vol = []

    # for filename in os.listdir('datasets/stocks'):
    #     df = pandas.read_csv('datasets/stocks/{}'.format(filename))
    for ticker in allset:
        df = yf.download(ticker+".BK",start, end)
        try:
            if is_consolidating(df, percentage=7): 
                #data.append("{}".format(filename))
                data.append(ticker)
                price_now.append(get_price(df))
                volume.append(get_volume(df))
                avg_vol.append(get_volume_last5(df))


        except Exception as e:
                print('Error: ', str(e))

    df1 = pandas.DataFrame(data, columns = ['Name'])

    df2 = df1.assign(Price = price_now)

    df3 = df2.assign(Volume = volume)

    df4 = df3.assign(Avg = avg_vol)

    df4.to_csv(f'./daily_stock/consolidate/{end}'+'.csv')

    print(df4)



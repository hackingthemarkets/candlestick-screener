import talib
import numpy as np
import yfinance as yf 
import os, pandas
import datetime
import time
from set_stock import *

class Doji:

    def __init__(self, symbols):
        self.symbols = symbols

        start = "2021-05-10"
        # end = datetime.datetime.now()
        end = "2021-09-9"

        stock = []
        change = []
        current = []
        volume = []
       
        def current_open(data):
            current_open = data[-1:]
            current_open = current_open['Open'].values[0]
            return current_open

        def previous_close(data):   
            previous_close = data[-2:]
            previous_close = previous_close['Close'].values[0]
            previous_close = float("{:.2f}".format(previous_close))
            return previous_close

        def previous_lowest(data):
            previous_lowest = data[-2:]
            previous_lowest = previous_lowest['Low'].values[0]
            previous_lowest = float("{:.2f}".format(previous_lowest))
            return previous_lowest

        def current_close(data):
            current_close = data[-1:]
            current_close = current_close['Close'].values[0]
            return current_close

        def bullish_candle(data):
            if current_close(data) > current_open(data):
                return True

        def get_change(data):
            if current_close(data) > previous_close(data):
                change = current_close(data) - previous_close(data)
                return change

        def last_week_close_min(data):
            data = data.tail(5)
            data = data.iloc[0:7]
            data = data['Close']
            min_close = np.min(data)
            return min_close

        def lowest_close_min(data):
            data = data.tail(5)
            data = data.iloc[0:4]
            data = data['Low']
            lowest_close = np.min(data)
            return lowest_close

        def current_volume(data):
            current_volume = data[-1:]
            current_volume = current_volume['Volume'].values[0]
            return current_volume

    

        for ticker in symbols:
            data = yf.download(ticker+".BK",start, end)
            try:
                if current_close(data) <  lowest_close_min(data): 
                # and bullish_candle(data):

                    stock.append(ticker)
                   
                    current.append(current_close(data))

                    volume.append(current_volume(data))

            except Exception as e:
                    print('Error: ', str(e))

        df = pandas.DataFrame(stock, columns=['Name'])
        # df1 = df.assign(Change = change)
        df2 = df.assign(Price = current)
        df3 = df2.assign(Volume = volume)
        df3.to_csv('./daily_stock/pull_back/pull_back8sep'+'.csv')

        print(df3)
        print(stock)

    

doji = Doji(allset)
print(doji)


###--------------- No class -------------###

# start = "2021-04-10"
# end = datetime.datetime.now()
# end = "2021-06-1"
# def previous_close(data):   
#     previous_close = data[-2:]
#     previous_close = previous_close['Close'].values[0]
#     previous_close = float("{:.2f}".format(previous_close))
#     return previous_close
# def current_close(data):
#     current_close = data[-1:]
#     current_close = current_close['Close'].values[0]
#     return current_close
# def get_change(data):
#     if current_close(data) > previous_close(data):
#         change = current_close(data) - previous_close(data)
#         return change
# stock = []
# for ticker in test:
#     data = yf.download(ticker+".BK",start, end)

#     if get_change(data):

#         stock.append(ticker)
  

# print(stock)

# def current_vol(data):
#     current_vol = data[-1:]
#     current_vol = current_vol['Volume'].values[0]
#     return current_vol

# def current_close(data):
#     current_close = data[-1:]
#     current_close = current_close['Close'].values[0]
#     return current_close

# def avg_vol5(data):
#     data = data.tail(6)
#     data = data.iloc[0:5]
#     data = data['Volume']
#     avg_vol5 = np.mean(data)
#     return avg_vol5

# def last_week_close_min(data):
#     data = data.tail(7)
#     data = data.iloc[0:6]
#     data = data['Close']
#     min_close = np.min(data)
#     return min_close


# def pct_cmpr(data):
#     cmpr = current_vol(data) / avg_vol5(data) * 100
#     return cmpr 
   
# symbols = []

# data = yf.download("PLANET.BK",start, end)
# if current_close(data) < last_week_close_min(data):
#     print(current_close(data))








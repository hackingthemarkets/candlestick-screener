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

        start = "2021-06-10"
        end = datetime.datetime.now()

        stock = []
        change = []
        current = []
       
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

        def get_change(data):
            if current_close(data) > current_open(data):
                change = current_close(data) - current_open(data)
                return change
            

        def last_week_close_min(data):
            data = data.tail(7)
            data = data.iloc[0:6]
            data = data['Close']
            min_close = np.min(data)
            return min_close

        def lowest_close_min(data):
            data = data.tail(7)
            data = data.iloc[0:6]
            data = data['Low']
            lowest_close = np.min(data)
            return lowest_close

        for ticker in symbols:
            data = yf.download(ticker+".BK",start, end)
            try:
                changed = current_close(data) - current_open(data)
                stock.append(ticker)
                change.append(changed)
                current.append(current_close(data))

            except Exception as e:
                    print('Error: ', str(e))

        df = pandas.DataFrame(stock, columns=['Name'])
        df1 = df.assign(Change = change)
        df2 = df1.assign(Price = current)
        df2.to_csv('./daily_stock/changed2sep'+'.csv')

        print(df2)


    

doji = Doji(allset)
print(doji)
import talib
import yfinance as yf 
import os, pandas
import datetime
import time
import datetime
import random
from urllib.request import urlopen

import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas_datareader.data as web
import pylab
from mplfinance.original_flavor import candlestick_ohlc
from set_stock import *
from stock import Stock

industrials = []

# If stocks array is empty, pull stock list from stocks.txt file
stocks = stocks if len(industrials) > 0 else [
    line.rstrip() for line in open("industrials.txt", "r")]

# Time frame you want to pull data from
start = datetime.datetime.now()-datetime.timedelta(days=365)
end = datetime.datetime.now()


if __name__ == "__main__":

    # Array of moving averages you want to get
    MAarr = [20, 50]

    allData = []
    
    for ticker in stocks:

        try:
            data = []
            
            print("Pulling data for " + ticker)

            stock = Stock(ticker+".BK", start, end)

            # Append data to array
            data.append(ticker.upper())

            data.append(stock.closes[-1])

            data.append(stock.volumes[-1])

            for MA in MAarr:
                computedSMA = stock.SMA(period=MA)
                #check ema20 < ema50
                
                # print(computedEMA)
                data.append(computedSMA[-1])
            
            currentRsi = float("{:.2f}".format(stock.rsi[-1]))


            if currentRsi > 70:
                data.append(str(currentRsi))
            
            else:
                data.append(currentRsi)

            allData.append(data)
            df = pandas.DataFrame(allData, columns=['Stock', 'Price', 'Volume', '20SMA', '50SMA', 'RSI'])
            df['compare'] = np.where((df['20SMA'] < df['50SMA'] ), True, False)
            
            
            df2 = pandas.DataFrame(df, columns=['Stock', 'Price', 'Volume', '20SMA', '50SMA', 'RSI', 'compare'] )
            
            drop_false = df2[ df2['compare'] != True ].index
        
            df2.drop(drop_false, inplace = True)


                    
                
        except Exception as e:
            print('Error: ', str(e))
    df2.to_csv('./daily_stock/sma15aug'+'.csv')
    print(df2)
    
  

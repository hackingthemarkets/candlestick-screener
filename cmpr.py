import talib
import numpy as np
import yfinance as yf 
import os, pandas
import datetime
import time
from set_stock import *



start = "2021-06-1"
end = datetime.datetime.now()
# end = "2021-05-13"

def current_vol(data):
    current_vol = data[-1:]
    current_vol = current_vol['Volume'].values[0]
    return current_vol

def avg_vol5(data):
    data = data.tail(6)
    data = data.iloc[0:5]
    data = data['Volume']
    avg_vol5 = np.mean(data)
    return avg_vol5

def current_close(data):
    current_close = data[-1:]
    current_close = current_close['Close'].values[0]
    return current_close


def pct_cmpr(data):
    
    cmpr = current_vol(data) / avg_vol5(data) * 100
   
    return cmpr 
   
symbols = []
pct = []
price = []
volume = []

for ticker in allset:
    data = yf.download(ticker+".BK",start, end)
    try:
        if current_vol(data) > 0 \
            or current_vol(data) != 'nan':

            if pct_cmpr(data) > 200:
                symbols.append(ticker)
                pct.append(pct_cmpr(data))
                price.append(current_close(data))
                volume.append(current_vol(data))
    except Exception as e:
            print('Error: ', str(e))

df = pandas.DataFrame(symbols, columns=['Ticker'])
df1 = df.assign(pctcmpr = pct)
df2 = df1.assign(Price = price)
df3 = df2.assign(Volume = volume)
df3.to_csv(f'./daily_stock/pct_cmpr/{end}'+'.csv')

print(df3)

# symbols.append(ticker)
# volume.append(current_vol(data))

# df = pandas.DataFrame(ticker)
# df2 = df.assign(volume)
# print(df2)

# data = yf.download("JAS.BK",start, end)
# data = data.tail(7)
# data = data.iloc[0:6]
# data = data['Close']
# min_close = np.min(data)
# print(min_close)
# print(data)
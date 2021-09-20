import talib
import numpy as np
import yfinance as yf 
import os, pandas
import datetime
import time
from set_stock import *

start = "2021-05-01"
# end = datetime.datetime.now()
end = "2021-06-15"

def is_bullish_previousday(data):
    if current_open(data) > previous_close(data) \
        and current_close(data) < previous_open(data):

        return True

    return False

    
def is_bearish_previousday(data):
    if previous_close(data) < previous_open(data):
        return True

    return False

def is_bullish_engulfing(data):

    if is_bearish_previousday(data) \
        and current_close(data) > previous_open(data) \
        and current_open(data) < previous_close(data):
        return True
    return False

def is_bearish_engulfing(data):

    if is_bullish_previousday(data) \
        and current_open(data) > previous_close(data) \
        and current_close(data) < previous_open(data):
        return True
    return False

def current_open(data):
    current_open = data[-1:]
    current_open = current_open['Open'].values[0]

    return current_open

def current_close(data):
    current_close = data[-1:]
    current_close = current_close['Close'].values[0]

    return current_close

def current_lowest(data):
    current_lowest = data[-1:]
    current_lowest = current_lowest['Low'].values[0]

def current_highest(data):
    current_highest = data['High'].values[0]

    return current_highest

def previous_open(data):
    previous_open = data[-2:]
    previous_open = previous_open['Open'].values[0]

    return previous_open

def previous_close(data):
    previous_close = data[-2:]
    previous_close = previous_close['Close'].values[0]
    
    return previous_close

def last2_close(data):
    last2_close = data[-3:]
    last2_close = last2_close['Close'].values[0]
    return last2_close

def last3_close(data):
    last3_close = data[-4:]
    last3_close = last3_close['Close'].values[0]
    return last3_close

def last4_close(data):
    last4_close = data[-5:]
    last4_close = last4_close['Close'].values[0]
    return last4_close

def last5_close(data):
    last5_close = data[-6:]
    last5_close = last5_close['Close'].values[0]
    return last5_close

def last_week_close_min(data):
    data = data.tail(7)
    data = data.iloc[0:6]
    data = data['Close']
    min_close = np.min(data)
    return min_close

# def is_bearish(data):
#     if is_bearish_previousday(data) \
#         and current_close(data) < last_week_close_min(data):

#         return True
#     return False


bearish = []
current_price = []
previous_price = []
stochastic = []

for ticker in bear:
    data = yf.download(ticker+".BK",start, end)
    try:
        if is_bearish_previousday(data) \
            and current_close(data) < last_week_close_min(data):

            bearish.append(ticker)
            current_price.append(current_close(data))

    except Exception as e:
            print('Error: ', str(e))
        


df = pandas.DataFrame(bearish, columns=['Bearish'])
df1 = df.assign(Price = current_price)
df1.to_csv('./daily_stock/bearish'+'.csv')
print(df1)













import yfinance as yf 
import numpy as np
import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt
from set_stock import *


### ------------------------------------------------------------------------###
# Scan engulfing candle.

# Scan current volume compare to last week(last 5 days)

# Scan %cmpr to find which ticker is about to go.

# Scan consolidating candles last 10 days and inspect average volume should present a momentum (big volume) to check that there are potentail to go.

### ------------------------------------------------------------------------###


    
start = "2021-05-01"
end = datetime.datetime.now()
#end = "2021-05-14"

def is_bullish(data):
    if current_open(data) > previous_close(data) \
        and current_close(data) < previous_open(data):
        return True
    return False

# Check 2 previous candles
def is_bearish_2daysago(data):
    if twoday_ago_close(data) < twoday_ago_open(data):
        return True
    return False

def is_bearish_previousday(data):
    if previous_close(data) < previous_open(data):
        return True
    return False

def is_bullish_engulfing(data):     # 3 previou candles are bearish, and the body of the current one is cover low and high of the previous.
    if is_bearish_previousday(data) \
        and current_close(data) > previous_open(data) \
        and current_open(data) < previous_close(data): 
        return True
    return False

def is_hammer(data):
    if is_bearish_previousday(data) \
        and current_open(data) == current_highest(data) \
        and current_close(data) < current_open(data)\
        and current_close(data) > current_lowest(data): 
        return True
    return False

def is_morning_star(data):         # current candle is open and close lower than previous candle and 3-4 previous candles should be bearish.
    if is_bearish_previousday(data) \
        and current_highest(data) < previous_lowest(data) \
        and current_lowest(data) < previous_lowest(data):
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
    current_lowest = float("{:.2f}".format(current_lowest))
    return current_lowest

def current_highest(data):
    current_highest = data[-1:]
    current_highest = current_highest['High'].values[0]
    current_highest = float("{:.2f}".format(current_highest))
    return current_highest

def previous_open(data):
    previous_open = data[-2:]
    previous_open = previous_open['Open'].values[0]
    previous_open = float("{:.2f}".format(previous_open))
    return previous_open

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

def twoday_ago_close(data):
    twoday_ago_close = data[-3:]
    twoday_ago_close = twoday_ago_close['Close'].values[0]
    return twoday_ago_close

def twoday_ago_open(data):
    twoday_ago_open = data[-3:]
    twoday_ago_open = twoday_ago_open['Open'].values[0]
    return twoday_ago_open

#consolidating graph
def is_consolidating(data, percentage=5):
        recent_candlesticks = data[-15:]

        max_close = recent_candlesticks['Close'].max()
        min_close = recent_candlesticks['Close'].min()
    

        threshold = 1 - (percentage / 100)
        if min_close > (max_close * threshold):
            return True        

        return False

def get_volume(data):
    current_volume = data[-1:]
    volume = current_volume['Volume'].values[0]
    return volume

def get_volume_last5(data):
    vol = data.tail(6)
    vol = vol.iloc[0:5]
    vol = vol['Volume']
    avg_vol5 = np.mean(vol)
    return avg_vol5
  
def is_breaking_out(data, percentage=2.5):
    last_close = data[-1:]['Close'].values[0]
    if is_consolidating(data[:-1], percentage=percentage):
        recent_closes = data[-16:-1]
        if last_close > recent_closes['Close'].max():
            return True
    return False

data = []
price_now = []
volume = []
avg_vol = []

engulfing = []
eng_current = []
hammer = []
ham_current = []
morning_star = []
morning_current =[]



for ticker in allset:
    data = yf.download(ticker+".BK",start, end)
    try:
        if is_bullish_engulfing(data):    #check previous day is bearish and current day is bullish engulfing
            engulfing.append(ticker)
            eng_current.append(current_close(data))
        elif is_hammer(data):
            hammer.append(ticker)
            ham_current.append(current_close(data))
        elif is_morning_star(data):
            morning_star.append(ticker)  
            morning_current.append(current_close(data))
        elif is_consolidating(data, percentage=10):
            data.append(ticker)
            price_now.append(current_close(data))
            volume.append(get_volume(data))
            avg_vol.append(get_volume_last5(data))
        
    except Exception as e:
            print('Error: ', str(e))
    

eng = pandas.DataFrame(engulfing, columns=['Engulfing'])
engf = eng.assign(Price = eng_current)
engf.to_csv(f'./daily_stock/engulfing/{end}'+'.csv')
print(engf)

ham = pandas.DataFrame(hammer, columns=['Hammer'])
hamr = ham.assign(Price = ham_current)
hamr.to_csv(f'./daily_stock/hammer/{end}'+'.csv')
print(hamr)

doji = pandas.DataFrame(morning_star, columns=['MorningStar'])
doji1 = doji.assign(Price = morning_current)
doji1.to_csv(f'./daily_stock/morningstar/star{end}'+'.csv')
print(doji1)

conso = pandas.DataFrame(data, columns = ['Name'])
consol = conso.assign(Price = price_now)
consol2 = consol.assign(Volume = volume)
consol3 = consol2.assign(Avg = avg_vol)
consol3.to_csv(f'./daily_stock/consolidate/{end}'+'.csv')
print(consol3)
        
    





    



    
    

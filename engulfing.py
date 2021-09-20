import numpy as np
import yfinance as yf 
import os, pandas
import datetime
import time
from set_stock import *

# class engulfing_candle:

#     start = "2021-05-01"
#     end = datetime.datetime.now()
#     #end = "2021-05-14"

#     def is_bullish(data):
#         if current_open(data) > previous_close(data) \
#             and current_close(data) < previous_open(data):
#             return True
#         return False

#     # Check 2 previous candles
#     def is_bearish_2daysago(data):
#         if twoday_ago_close(data) < twoday_ago_open(data):
#             return True
#         return False

#     def is_bearish_previousday(data):
#         if previous_close(data) < previous_open(data):
#             return True
#         return False

#     def is_bullish_engulfing(data):     # 3 previou candles are bearish, and the body of the current one is cover low and high of the previous.
#         if is_bearish_previousday(data) \
#             and current_close(data) > previous_open(data) \
#             and current_open(data) < previous_close(data): 
#             return True
#         return False

#     def is_hammer(data):
#         if is_bearish_previousday(data) \
#             and current_open(data) == current_highest(data) \
#             and current_close(data) < current_open(data)\
#             and current_close(data) > current_lowest(data): 
#             return True
#         return False

#     def is_morning_star(data):         # current candle is open and close lower than previous candle and 3-4 previous candles should be bearish.
#         if is_bearish_previousday(data) \
#             and current_highest(data) < previous_lowest(data) \
#             and current_lowest(data) < previous_lowest(data):
#             return True
#         return False

#     def current_open(data):
#         current_open = data[-1:]
#         current_open = current_open['Open'].values[0]
#         return current_open

#     def current_close(data):
#         current_close = data[-1:]
#         current_close = current_close['Close'].values[0]
#         return current_close

#     def current_lowest(data):
#         current_lowest = data[-1:]
#         current_lowest = current_lowest['Low'].values[0]
#         current_lowest = float("{:.2f}".format(current_lowest))
#         return current_lowest

#     def current_highest(data):
#         current_highest = data[-1:]
#         current_highest = current_highest['High'].values[0]
#         current_highest = float("{:.2f}".format(current_highest))
#         return current_highest

#     def previous_open(data):
#         previous_open = data[-2:]
#         previous_open = previous_open['Open'].values[0]
#         previous_open = float("{:.2f}".format(previous_open))
#         return previous_open

#     def previous_close(data):   
#         previous_close = data[-2:]
#         previous_close = previous_close['Close'].values[0]
#         previous_close = float("{:.2f}".format(previous_close))
#         return previous_close

#     def previous_lowest(data):
#         previous_lowest = data[-2:]
#         previous_lowest = previous_lowest['Low'].values[0]
#         previous_lowest = float("{:.2f}".format(previous_lowest))
#         return previous_lowest

#     def twoday_ago_close(data):
#         twoday_ago_close = data[-3:]
#         twoday_ago_close = twoday_ago_close['Close'].values[0]
#         return twoday_ago_close

#     def twoday_ago_open(data):
#         twoday_ago_open = data[-3:]
#         twoday_ago_open = twoday_ago_open['Open'].values[0]
#         return twoday_ago_open

#     engulfing = []
#     eng_current = []
#     hammer = []
#     ham_current = []
#     morning_star = []
#     morning_current =[]



#     for ticker in allset:
#         data = yf.download(ticker+".BK",start, end)
#         try:
#             if is_bullish_engulfing(data):    #check previous day is bearish and current day is bullish engulfing
#                 engulfing.append(ticker)
#                 eng_current.append(current_close(data))
#             elif is_hammer(data):
            
#                 hammer.append(ticker)
#                 ham_current.append(current_close(data))
#             elif is_morning_star(data):
            
#                 morning_star.append(ticker)  
#                 morning_current.append(current_close(data))
#         except Exception as e:
#                 print('Error: ', str(e))
    
# # df = pandas.DataFrame(engulfing, columns=['Bullish', 'Price'])
# # print(df)

#     eng = pandas.DataFrame(engulfing, columns=['Engulfing'])
#     df = eng.assign(Price = eng_current)
#     df.to_csv('./daily_stock/engulfing31'+'.csv')
#     print(df)

#     ham = pandas.DataFrame(hammer, columns=['Hammer'])
#     df1 = ham.assign(Price = ham_current)
#     df1.to_csv('./daily_stock/hammer31'+'.csv')
#     print(df1)

#     doji = pandas.DataFrame(morning_star, columns=['MorningStar'])
#     df2 = doji.assign(Price = morning_current)
#     df2.to_csv('./daily_stock/morningStar31'+'.csv')
#     print(df2)

start = "2021-05-01"
end = datetime.datetime.now()
# end = "2021-07-04"

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
        and current_open(data) < previous_close(data) \
        and current_close(data) > previous_open(data): 
        return True
    return False

def is_hammer(data):
    if is_bearish_previousday(data) \
        and current_open(data) == current_highest(data) \
        and current_close(data) < current_open(data)\
        and close_above_lowest_80pct(data, percentage=0.7):  #current close must be higer that lowest 80%
        return True
    return False

def is_morning_star(data):         # current candle is open and close lower than previous candle and 3-4 previous candles should be bearish.
    if is_bearish_previousday(data) \
        and current_close(data) < previous_close(data) \
        and current_open(data) < previous_close(data):
        return True
    return False

def close_above_lowest_80pct(data, percentage=0.7):
    if current_open(data) > current_close(data):
        gap = current_highest(data) - current_lowest(data)
        # pct = 1 - (percentage / 100)
        ratio = (gap * percentage) + current_lowest(data)
        if current_close(data) > ratio: # > low + 80%
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
    # previous_open = float("{:.2f}".format(previous_open))
    return previous_open

def previous_close(data):   
    previous_close = data[-2:]
    previous_close = previous_close['Close'].values[0]
    # previous_close = float("{:.2f}".format(previous_close))
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

def last_week_close_min(data):
    data = data[-5:]
    data = data.iloc[0:4]
    min_close = data['Close'].min()
    return min_close

def current_volume(data):
    current_volume = data[-1:]
    current_volume = current_volume['Volume'].values[0]
    return current_volume

engulfing = []
eng_current = []
hammer = []
ham_current = []
morning_star = []
morning_current =[]
volume_eng = []
volume_ham = []
volume_doji = []



for ticker in allset:
    data = yf.download(ticker+".BK",start, end)
    try:
        if is_bullish_engulfing(data):    #check previous day is bearish and current day is bullish engulfing
            engulfing.append(ticker)
            eng_current.append(current_close(data))
            volume_eng.append(current_volume(data))
        elif is_hammer(data):
            hammer.append(ticker)
            ham_current.append(current_close(data))
            volume_ham.append(current_volume(data))
        elif is_morning_star(data):
            morning_star.append(ticker)  
            morning_current.append(current_close(data))
            volume_doji.append(current_volume(data))
    except Exception as e:
            print('Error: ', str(e))
    
# df = pandas.DataFrame(engulfing, columns=['Bullish', 'Price'])
# print(df)

eng = pandas.DataFrame(engulfing, columns=['Engulfing'])
eng1 = eng.assign(Price = eng_current)
eng2 = eng1.assign(Volume = volume_eng)
eng2.to_csv(f'./daily_stock/engulfing/{end}'+'.csv')
print(eng2)

ham = pandas.DataFrame(hammer, columns=['Hammer'])
ham1 = ham.assign(Price = ham_current)
ham2 = ham1.assign(Volume = volume_ham)
ham2.to_csv(f'./daily_stock/hammer/{end}'+'.csv')
print(ham2)

doji = pandas.DataFrame(morning_star, columns=['MorningStar'])
doji1 = doji.assign(Price = morning_current)
doji2 = doji1.assign(Volume = volume_doji)
doji2.to_csv(f'./daily_stock/morningstar/star{end}'+'.csv')
print(doji2)

print(morning_star)
print(hammer)
print(engulfing)

















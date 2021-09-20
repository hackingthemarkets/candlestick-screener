import yfinance as yf 
import numpy as np
import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt

from set_stock import *

class volume_increased:
     
    def __init__(self, symbols):
        self.symbols = symbols

        start = "2021-01-01"
        end = datetime.datetime.now()
        # end = "2021-06-03"

        def current_volume(data):
            current_volume = data[-1:]
            current_volume = current_volume['Volume'].values[0]
            return current_volume

        def volume_lastweek(data):
            volume_lastweek = data[-5:]
            volume_lastweek = volume_lastweek['Volume'].values[0]
            return volume_lastweek

        def avg_vol5(data):
            data = data.tail(6)
            data = data.iloc[0:5]
            data = data['Volume']
            avg_vol5 = np.mean(data)
            return avg_vol5

        def volume_yesterday(data):
            volume_yesterday = data[-2:]
            volume_yesterday = volume_yesterday['Volume'].values[0]
            return volume_yesterday
        
        def previous_close(data):   
            previous_close = data[-2:]
            previous_close = previous_close['Close'].values[0]
            previous_close = float("{:.2f}".format(previous_close))
            return previous_close

        def diff_price(data):
            diff = price(data) - previous_close(data)
            diff = float("{:.2f}".format(diff))
            return diff

        def price(data):
            price = data[-1:]
            price = price['Close'].values[0]
            return price

        increased_symbol = []
        volume = []
        avg_vol = []
        change = []
        current_price = []

        for ticker in symbols:
            data = yf.download(ticker+".BK",start, end)
            try:
                if current_volume(data) > avg_vol5(data):
                    increased_symbol.append(ticker)
                    volume.append(current_volume(data))
                    avg_vol.append(avg_vol5(data))
                    change.append(diff_price(data))
                    current_price.append(price(data))

            except Exception as e:
                    print('Error: ', str(e))

        df = pd.DataFrame(increased_symbol, columns = ['Symbols'])
        df2 = df.assign(Vol = volume)
        df3 = df2.assign(Avg = avg_vol)
        df4 = df3.assign(Chg = change)
        df5 = df4.assign(Price = current_price)
        df5.to_csv(f'./daily_stock/volume/{end}' + '.csv')
        print(df5)

volumetoday = volume_increased(allset)
print(volumetoday)

    
    
    
    
    
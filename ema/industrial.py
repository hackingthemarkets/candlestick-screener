#!/usr/bin/env python3

import datetime
import random
import time
from urllib.request import urlopen

import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas_datareader.data as web
import pylab
from mplfinance.original_flavor import candlestick_ohlc
from pandas.core.common import flatten
from tabulate import tabulate

from stock import Stock

matplotlib.rcParams.update({'font.size': 9})

industrials = []

# If stocks array is empty, pull stock list from stocks.txt file
stocks = stocks if len(industrials) > 0 else [
    line.rstrip() for line in open("industrials.txt", "r")]

# Time frame you want to pull data from
start = datetime.datetime.now()-datetime.timedelta(days=365)
end = datetime.datetime.now()

if __name__ == "__main__":

    # Array of moving averages you want to get
    MAarr = [20, 50, 200]

    allData = []

    for ticker in stocks:

        try:
            data = []

            print("Pulling data for " + ticker)

            stock = Stock(ticker, start, end)

            # Append data to array
            data.append(ticker.upper())

            data.append(stock.closes[-1])

            for MA in MAarr:
                computedSMA = stock.SMA(period=MA)
                # print(computedSMA)
                data.append(computedSMA[-1])

            currentRsi = float("{:.2f}".format(stock.rsi[-1]))

            if currentRsi > 70:
                data.append(str(currentRsi) + " 🔥")
            elif currentRsi >= 50 and currentRsi < 60:
                data.append(str(currentRsi) + " \U0001f600")
            elif currentRsi < 40:
                data.append(str(currentRsi) + " 🧊")
            else:
                data.append(currentRsi)

            #chartLink = "https://finance.yahoo.com/quote/" + ticker + "/chart?p=" + ticker
            chartLink = "https://finance.yahoo.com/quote/" + ticker + "/"
            

            data.append(chartLink)

            allData.append(data)

            # Shows chart only if current RSI is greater than or less than 70 or 30 respectively
            # if currentRsi < 30 or currentRsi > 70:

            #     stock.graph(MAarr)

        except Exception as e:
            print('Error: ', str(e))

    print(tabulate(allData, headers=flatten([
        'Stock', 'Price', [str(x) + " MA" for x in MAarr], "RSI", "Chart"])))



    
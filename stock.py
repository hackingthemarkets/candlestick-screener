#!/usr/bin/env python3

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

matplotlib.rcParams.update({'font.size': 9})


class Stock:

    ticker = None
    dates = None
    closes = None
    highs = None
    lows = None
    opens = None
    volumes = None
    rsi = None

    def __init__(self, ticker, start, end=datetime.datetime.now()):
        self.ticker = ticker

        """
        Different sources for pulling data can be found here:
        https://readthedocs.org/projects/pandas-datareader/downloads/pdf/latest/
        """

        stockData = web.DataReader(ticker, 'yahoo', start, end)

        self.dates = [mdates.date2num(d) for d in stockData.index]
        self.closes = stockData['Close']
        self.highs = stockData['High']
        self.lows = stockData['Low']
        self.opens = stockData['Open']
        self.volumes = stockData['Volume']

        self.rsi = self.RSI(self.closes)

    def RSI(self, prices, n=14):
        deltas = np.diff(prices)
        seed = deltas[:n+1]
        up = seed[seed >= 0].sum()/n
        down = -seed[seed < 0].sum()/n
        rs = up/down
        rsi = np.zeros_like(prices)
        rsi[:n] = 100. - 100./(1.+rs)

        for i in range(n, len(prices)):
            delta = deltas[i-1]  # The diff is 1 shorter

            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta

            up = (up*(n-1) + upval)/n
            down = (down*(n-1) + downval)/n

            rs = up/down
            rsi[i] = 100. - 100./(1.+rs)

        return rsi

    def SMA(self, period, values=None):

        values = self.closes if values is None else values

        """
        Simple Moving Average. Periods are the time frame. For example, a period of 50 would be a 50 day
        moving average. Values are usually the stock closes but can be passed any values
        """

        weigths = np.repeat(1.0, period)/period
        smas = np.convolve(values, weigths, 'valid')
        return smas  # as a numpy array

    def EMA(self, period, values=None):

        values = self.closes if values is None else values

        """
        Exponential Moving Average. Periods are the time frame. For example, a period of 50 would be a 50 day
        moving average. Values are usually the stock closes but can be passed any values
        """

        weights = np.exp(np.linspace(-1., 0., period))
        weights /= weights.sum()
        a = np.convolve(values, weights, mode='full')[:len(values)]
        a[:period] = a[period]
        return a

    def MACD(self, x, slow=26, fast=12):
        """
        Compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
        return value is emaslow, emafast, macd which are len(x) arrays
        """

        emaslow = self.EMA(slow, x)
        emafast = self.EMA(fast, x)
        return emaslow, emafast, emafast - emaslow

    def graph(self, movingAverageArr=[]):
        try:

            x = 0
            y = len(self.dates)
            newAr = []
            while x < y:
                appendLine = self.dates[x], self.opens[x], self.closes[x], self.highs[x], self.lows[x], self.volumes[x]
                newAr.append(appendLine)
                x += 1

            # Fix this
            SP = len(self.dates[200-1:])

            fig = plt.figure(facecolor='#07000d')

            ax1 = plt.subplot2grid(
                (6, 4), (1, 0), rowspan=4, colspan=4, facecolor='#07000d')
            candlestick_ohlc(ax1, newAr[-SP:], width=.6,
                             colorup='#53c156', colordown='#ff1717')

            for MA in movingAverageArr:

                computedSMA = self.SMA(MA, self.closes)

                # Used to generate random hex color to put on graph
                def r(): return random.randint(0, 255)
                randomColor = '#%02X%02X%02X' % (r(), r(), r())

                maLabel = str(MA) + ' SMA'
                ax1.plot(self.dates[-SP:], computedSMA[-SP:], randomColor,
                         label=maLabel, linewidth=1.5)

            ax1.grid(False, color='w')
            ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
            ax1.xaxis.set_major_formatter(
                mdates.DateFormatter('%Y-%m-%d'))
            ax1.yaxis.label.set_color("w")
            ax1.spines['bottom'].set_color("#5998ff")
            ax1.spines['top'].set_color("#5998ff")
            ax1.spines['left'].set_color("#5998ff")
            ax1.spines['right'].set_color("#5998ff")
            ax1.tick_params(axis='y', colors='w')
            plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
            ax1.tick_params(axis='x', colors='w')
            plt.ylabel('Stock price and Volume')

            maLeg = plt.legend(loc=9, ncol=2, prop={'size': 7},
                               fancybox=True, borderaxespad=0.)
            maLeg.get_frame().set_alpha(0.4)
            textEd = pylab.gca().get_legend().get_texts()
            pylab.setp(textEd[0:5], color='w')

            volumeMin = 0

            ax0 = plt.subplot2grid(
                (6, 4), (0, 0), sharex=ax1, rowspan=1, colspan=4, facecolor='#07000d')

            rsiCol = '#c1f9f7'
            posCol = '#386d13'
            negCol = '#8f2020'

            ax0.plot(self.dates[-SP:], self.rsi[-SP:],
                     rsiCol, linewidth=1.5)
            ax0.axhline(70, color=negCol)
            ax0.axhline(30, color=posCol)
            ax0.fill_between(self.dates[-SP:], self.rsi[-SP:], 70, where=(self.rsi[-SP:]
                                                                          >= 70), facecolor=negCol, edgecolor=negCol, alpha=0.5)
            ax0.fill_between(self.dates[-SP:], self.rsi[-SP:], 30, where=(self.rsi[-SP:]
                                                                          <= 30), facecolor=posCol, edgecolor=posCol, alpha=0.5)
            ax0.set_yticks([30, 70])
            ax0.yaxis.label.set_color("w")
            ax0.spines['bottom'].set_color("#5998ff")
            ax0.spines['top'].set_color("#5998ff")
            ax0.spines['left'].set_color("#5998ff")
            ax0.spines['right'].set_color("#5998ff")
            ax0.tick_params(axis='y', colors='w')
            ax0.tick_params(axis='x', colors='w')
            plt.ylabel('RSI')

            ax1v = ax1.twinx()
            ax1v.fill_between(self.dates[-SP:], volumeMin,
                              self.volumes[-SP:], facecolor='#00ffe8', alpha=.4)
            ax1v.axes.yaxis.set_ticklabels([])
            ax1v.grid(False)

            # Edit this to 3, so it's a bit larger
            ax1v.set_ylim(0, 3*self.volumes.max())
            ax1v.spines['bottom'].set_color("#5998ff")
            ax1v.spines['top'].set_color("#5998ff")
            ax1v.spines['left'].set_color("#5998ff")
            ax1v.spines['right'].set_color("#5998ff")
            ax1v.tick_params(axis='x', colors='w')
            ax1v.tick_params(axis='y', colors='w')
            ax2 = plt.subplot2grid(
                (6, 4), (5, 0), sharex=ax1, rowspan=1, colspan=4, facecolor='#07000d')
            fillcolor = '#00ffe8'
            nslow = 26
            nfast = 12
            nema = 9
            emaslow, emafast, macd = self.MACD(self.closes)
            ema9 = self.EMA(nema, macd)
            ax2.plot(self.dates[-SP:], macd[-SP:],
                     color='#4ee6fd', lw=2)
            ax2.plot(self.dates[-SP:], ema9[-SP:],
                     color='#e1edf9', lw=1)
            ax2.fill_between(self.dates[-SP:], macd[-SP:]-ema9[-SP:], 0,
                             alpha=0.5, facecolor=fillcolor, edgecolor=fillcolor)

            plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
            ax2.spines['bottom'].set_color("#5998ff")
            ax2.spines['top'].set_color("#5998ff")
            ax2.spines['left'].set_color("#5998ff")
            ax2.spines['right'].set_color("#5998ff")
            ax2.tick_params(axis='x', colors='w')
            ax2.tick_params(axis='y', colors='w')
            plt.ylabel('MACD', color='w')
            ax2.yaxis.set_major_locator(
                mticker.MaxNLocator(nbins=5, prune='upper'))
            for label in ax2.xaxis.get_ticklabels():
                label.set_rotation(45)

            plt.suptitle(self.ticker.upper(), color='w')

            plt.setp(ax0.get_xticklabels(), visible=False)
            plt.setp(ax1.get_xticklabels(), visible=False)

            # ax1.annotate('Look Here!', (date[-1], Av1[-1]),
            #              xytext=(0.8, 0.9), textcoords='axes fraction',
            #              arrowprops=dict(facecolor='white', shrink=0.05),
            #              fontsize=14, color='w',
            #              horizontalalignment='right', verticalalignment='bottom')

            plt.subplots_adjust(left=.09, bottom=.14,
                                right=.94, top=.95, wspace=.20, hspace=0)

            plt.show()
            fig.savefig('example.png', facecolor=fig.get_facecolor())

        except Exception as e:
            print('Error graphing data: ', str(e))

    
    # Consolidating 

    def is_consolidating(self, percentage=5):
        recent_candlesticks = stock[-10:]

        max_close = recent_candlesticks['Close'].max()
        min_close = recent_candlesticks['Close'].min()
    

        threshold = 1 - (percentage / 100)
        if min_close > (max_close * threshold):
            return True        

        return False
    
    def get_avg_volume5days(self):
        avg = self.volumes
        avg = avg.tail(6)
        avg = avg.iloc[0:5]
        # avg = avg['Volume']
        avg_vol5 = np.mean(avg)
        return avg_vol5
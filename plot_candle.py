# import plotly.graph.objects as go 
import pandas as pd
import talib
import numpy as np
import yfinance as yf 
import os, pandas
import datetime
import time
import mplfinance as mpf
import matplotlib.pyplot as plt

start = "2020-06-01"
end = datetime.datetime.now()
# end = "2021-07-09"
# end = "2021-06-30"
tickers = ["AEC","AMANAH","ASAP","ASP","CGH","CHAYO","ECL","FNS","FSS","GBX","GL","IFS","KCAR","KGI","MBKET","MICRO","ML","NCAP","PE","PL","S11","SAK","THANI","TK","TNITY","UOBKH","XPG"]
for ticker in tickers:
    data = yf.download(ticker +".BK", start, end)
    candle = mpf.plot(data, type='candle', volume=True, mav=(5), title=ticker)

    # plt.savefig(f'./daily_stock/{ticker}' + '.png')
print(candle)




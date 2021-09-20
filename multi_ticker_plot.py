import yfinance as yf 
import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt
from set_stock import *

class multistock_display:

    def __init__(self, symbols):
        self.symbols = symbols

        start = "2020-01-01"
        end = datetime.datetime.now()

        col_list = []
        close_price = []

        data = pd.DataFrame(columns=col_list)

        for ticker in symbols:
            df = yf.download(ticker+".BK", start, end)
            col_list.append(ticker)
            data[ticker] = df['Close']
            close_price.append(data[ticker])

        data = pd.DataFrame(close_price)
        data = data.transpose()     #swap row to column
        data.plot(figsize=(10, 7))
        plt.legend()
        plt.title("Adjusted Close Price", fontsize=16)
        plt.ylabel('Price', fontsize=14)
        plt.xlabel('Year', fontsize=14)
        plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
        plt.show()

        # print(data)
chart = multistock_display(energ)
print(chart)
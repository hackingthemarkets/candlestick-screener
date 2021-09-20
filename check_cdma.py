import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import os
import glob
import numpy as np
import shutil	
import time
import matplotlib.dates as mdates
from os import listdir, makedirs
from os.path import isfile, join, exists
#from mpl_finance.date2num
from matplotlib.dates import DateFormatter, WeekdayLocator,DayLocator, MONDAY
#from mpl_finance import candlestick_ohlc
from tqdm import tqdm
    

# def get_stocks():
#     stock = pd.read_csv("stock/allstock.csv", usecols=['stock_list'])
#     for i in range(len(stock)):
#         temp_df = stock + ".csv"
#     return (temp_df)

def getFileNameInDir(EOD_file):
	onlyFiles = [ join(EOD_file,f) for f in listdir(EOD_file) if isfile(join(EOD_file, f)) ]
	return onlyFiles

def getHeaderFile(eodFiles):
	#eodFiles = getFileNameInDir(EOD_file)
	for f in eodFiles:
		df = pd.read_csv(f)
		df['ShortEMA'] = df['CLOSE'].ewm(span=12).mean() 
		return df

def count():
	eodFiles = getFileNameInDir(EOD_file)	
	#eodFiles = eodFiles[-1 * 2:]	


def calculate_macd(df):
	df['ShortEMA'] = df['CLOSE'].ewm(span=12).mean()       #short ema
	df['LongEMA'] = df['CLOSE'].ewm(span=26).mean()       #long ema
	df['MACD'] = df['ShortEMA'] - df['LongEMA']       #MACD line 
	df['Signal Line'] = df['MACD'].ewm(span=9).mean()
	#df['dif']= df['MACD'] - df['Signal Line']
	MACD = df['MACD']
	signal = df['Signal Line']
	n = len(signal)

	Signal = []
	if MACD[n-1] > signal[n-1]:
		value = "MACD is above the signal line now!!!"
		Signal.append(value)
	elif MACD[n-1] == signal[n-1]:
		value = "MACD is == signal line"
		Signal.append(value)
	else:
		value = "----Below-----"
		Signal.append(value)

	return (Signal)
	

stock_name = ["GEL.csv", "SAM.csv"]
DIR_CURRENT = os.path.dirname(__file__)
DIR_DATA = "test"

def csv():
	outputPath = DIR_DATA
	for i in range(0, len(stock_name)):
		dates = pd.date_range('2021-01-04', '2021-04-09') # only 2017 data testing for now
		df = pd.DataFrame(index=dates)
		dfStock = pd.read_csv("data/" + stock_name[i], index_col="DATE",parse_dates=True, usecols=['DATE', 'CLOSE'])
		df = dfStock[i]
		df = df.join(df)
		df = df.dropna()
		# filename = stock_name[i].format(outputPath)
		# df.to_csv(filename, index="DATE")

def main():
	
    for i in range(0, len(stock_name)):
	    dates = pd.date_range('2021-01-04', '2021-04-19') 
	    df = pd.DataFrame(index=dates)
	    dfStock = pd.read_csv("data/" + stock_name[i],index_col="DATE",parse_dates=True, usecols=['DATE', 'CLOSE'])
		n = len(dfStock)
		for y in n:
			df += dfStock[y]
	    	df = df.join(df)
	    	df = df.dropna()
			calculate_macd(df)
	print(calculate_macd(df))

        


if __name__ == "__main__":
    #print(calculate_macd(df))
	main()

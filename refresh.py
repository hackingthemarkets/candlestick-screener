import os, csv, sys
import yfinance as yf
import datetime

if __name__ == '__main__':
	if(len(sys.argv)<2):
		sys.exit('Usage: '+__file__+" [all|symbol]")
	symbol = sys.argv[1]

	if(symbol and symbol != 'all'):
		data = yf.download(symbol, start="2020-01-01", end=datetime.date.today())
		data.to_csv('datasets/daily/{}.csv'.format(symbol))

	if(symbol == 'all'):
		with open('datasets/symbols.csv') as f:
		    for line in f:
		        if "," not in line:
		            continue
		        symbol = line.split(",")[0]
		        data = yf.download(symbol, start="2020-01-01", end=datetime.date.today())
		        data.to_csv('datasets/daily/{}.csv'.format(symbol))	
		

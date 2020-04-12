import talib as ta
import matplotlib.pyplot as plt

plt.style.use('bmh')
import yfinance as yf

stock = 'AMZN'
aapl = yf.download(stock, '2000-1-1', '2020-4-10')
del aapl['Close']
#aapl.rename(columns={'Open': 'OPEN', 'High': 'HIGH', 'Low': 'LOW', 'Adj Close': 'CLOSE', 'Volume': 'Volume_BTC'}, inplace=True)
aapl.rename(columns={'Adj Close': 'Close', 'Volume': 'Volume_BTC'}, inplace=True)
aapl.to_excel("D:\Stock Market\Daily\Test\sa Stock\AMZN.xlsx", sheet_name=stock, index=True)

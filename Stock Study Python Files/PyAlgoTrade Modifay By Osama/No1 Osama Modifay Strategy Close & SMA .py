from __future__ import print_function

from pyalgotrade import strategy
from pyalgotrade.barfeed import quandlfeed
from pyalgotrade.technical import ma
import pandas as pd

'''
# 1- Import Data from Yahoo Finance
import yfinance as yf

stock = 'XOM'
aapl = yf.download(stock, '2010-1-1', '2020-4-10')
# 2-Export Data to folder in PC
aapl.to_csv("D:\Stock Study Excel Files\Input Excel Files\Stock USA\WIKI-XOM-2019-quandl.csv", index=True)


1-Buy Signal:(Close >SMA((15) If the adjusted close price is above the SMA(15) we enter a long position (we place a buy market order).
2- Sell Signal: (Close<SMA(15)  If a long position is in place, and the adjusted close price drops below the SMA(15) 
we exit the long position (we place a sell market order). '''

sma_strategy = []
sma_value = []


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        super(MyStrategy, self).__init__(feed, 1000)
        self.__position = None
        self.__instrument = instrument
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__sma = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod)

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at $%.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        if self.__sma[-1] is None:
            return

        bar = bars[self.__instrument]
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if bar.getPrice() > self.__sma[-1]:
                # Enter a buy market order for 10 shares. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, 10, True)
        # Check if we have to exit the position.
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            self.__position.exitMarket()


def run_strategy(smaPeriod):
    # Load the bar feed from the CSV file
    feed = quandlfeed.Feed()
    feed.addBarsFromCSV("xom", "D:\WIKI-XOM-2018-quandl.csv")

    # Evaluate the strategy with the feed.
    myStrategy = MyStrategy(feed, "xom", smaPeriod)
    myStrategy.run()
    print("Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity())
    return myStrategy.getBroker().getEquity()


for i in range(1, 29):
    run_strategy(i)
    sma_value.append(i)
    sma_strategy.append(run_strategy(i))
# data = list(zip(sma_value, sma_strategy))
d = {'SMA Value': sma_value, 'Final portfolio value': sma_strategy}  # create dataframe from dic  two columns from list
df = pd.DataFrame(d)
# df = pd.DataFrame(data, columns=['SMA Value', 'Final portfolio value'], )
df.index += 1
df.to_excel('D:\Stock Study Excel Files\Output Excel Files\Stock USA\SMA Strategy.xlsx', sheet_name="SMA Strategy",
            index=True, index_label='No')

print(df)

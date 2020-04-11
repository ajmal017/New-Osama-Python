import talib as ta
import pandas as pd
import ta
import glob
# Import Built-Ins
import logging
# Import Third-Party
import numpy as np
# Import Homebrew
import matplotlib.pyplot as plt

plt.style.use('bmh')
# Init Logging Facilities
log = logging.getLogger(__name__)

# Load data
glob.glob("D:\Stock Market\Daily\Test\*.xlsx")
for f in glob.glob('D:\Stock Market\Daily\Test\*.xlsx'):
    df = pd.read_excel(f)
    # Clean nan values
    df = ta.utils.dropna(df)
    # Add all ta features filling nans values
    df = ta.add_all_ta_features(df, "Open", "High", "Low", "Close", "Volume_BTC", fillna=True)

columns_names = list(df.columns.values)
indecators = list(df.columns[9:].values)
indecators = indecators[55]
indecators = [indecators]
indecators

df['Signal'] = 0
sell = []
buy = []
date_sell = []
date_buy = []
indecators
for indector in indecators:
    for y in range(100, len(df.index)):
        if df[indector].iloc[y] <= df['Close'].iloc[y] and (df[indector].iloc[y - 1] > df['Close'].iloc[y - 1]):
            first_buy_signal = y
            print(first_buy_signal)
            break

    for x in range(first_buy_signal - 1, len(df.index)):
        if df[indicator].iloc[x] >= df['Close'].iloc[x] and (df[indicator].iloc[x - 1] < df['Close'].iloc[x - 1]):
            df['Signal'].iloc[x] = 'Sell'
            sell.append(df['Close'].iloc[x])
            date_sell.append(df['Date'].iloc[x])

        elif df[indicator].iloc[x] <= df['Close'].iloc[x] and (df[indicator].iloc[x - 1] > df['Close'].iloc[x - 1]):
            df['Signal'].iloc[x] = 'Buy'
            buy.append(df['Close'].iloc[x])
            date_buy.append(df['Date'].iloc[x])
    sell.append(0)
    date_sell.append(0)
    profits = pd.DataFrame()
    profits['Buy'] = buy
    profits['Buy Date'] = date_buy
    profits['Sell'] = sell
    profits['Sell Date'] = date_sell
    profits['Profits'] = ((profits['Sell'] - profits['Buy']) / profits['Sell']) * 100
    profits.drop(profits.tail(1).index, inplace=True)  # drop last n rows
    # print(profits)

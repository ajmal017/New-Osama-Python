import talib
import pandas as pd
import ta
import glob

# Load data
glob.glob("D:\Stock Market\Daily\Test\*.xlsx")
for f in glob.glob('D:\Stock Market\Daily\Test\*.xlsx'):
    df = pd.read_excel(f)
    # Clean nan values
    df = ta.utils.dropna(df)
    # Add all ta features filling nans values
    df = ta.add_all_ta_features(df, "Open", "High", "Low", "Close", "Volume_BTC", fillna=True)
    df['Signal'] = 0
    sell = []
    buy = []
    date_sell = []
    date_buy = []
    for y in range(100, len(df.index)):
        if df['trend_psar'].iloc[y] <= df['Close'].iloc[y] and (df['trend_psar'].iloc[y - 1] > df['Close'].iloc[y - 1]):
            first_buy_signal = y
            print(first_buy_signal)
            break

    for x in range(first_buy_signal, len(df.index)):
        if df['trend_psar'].iloc[x] >= df['Close'].iloc[x] and (df['trend_psar'].iloc[x - 1] < df['Close'].iloc[x - 1]):
            df['Signal'].iloc[x] = 'Sell'
            sell.append(df['Close'].iloc[x])
            date_sell.append(df['Date'].iloc[x])

        elif df['trend_psar'].iloc[x] <= df['Close'].iloc[x] and (df['trend_psar'].iloc[x - 1] > df['Close'].iloc[x - 1]):
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
    profits['Profits'] = profits['Sell'] - profits['Buy']
    print(profits)

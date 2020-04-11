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
    sell=[]
    buy=[]
    date_sell=[]
    date_buy= []
    for x in range(4000, len(df.index)):
        if df['trend_psar'].iloc[x] >= df['Close'].iloc[x] and (df['trend_psar'].iloc[x - 1] < df['Close'].iloc[x - 1]):
            df['Signal'].iloc[x] = 'Sell'
            sell.append(df['Close'])
            date_sell.append(df['Date'].iloc[x])

        elif df['trend_psar'].iloc[x] <= df['Close'].iloc[x] and (df['trend_psar'].iloc[x - 1] > df['Close'].iloc[x - 1]):
            df['Signal'].iloc[x] = 'Buy'
            buy.append(df['Close'])
            date_buy.append(df['Date'].iloc[x])
    pinfit = pd.DataFrame()
    pinfit['Sell']=sell
    pinfit['Sell Date']=date_sell
    pinfit['Buy']=buy
    pinfit['Sell Buy'] = date_buy
    pinfit['Gane']=pinfit['Sell']-pinfit['Buy']
    print(pinfit)


# Export to Excel File
df.round(2).to_excel(f'{f}.xlsx', sheet_name="indicator Osama", index=False)
print('OK The Files Ready ')

import pandas as pd
import ta
import glob
# Import Built-Ins
import logging
# Import Third-Party
# Import Homebrew
import matplotlib.pyplot as plt

plt.style.use('bmh')
# Init Logging Facilities
log = logging.getLogger(__name__)
#################################################################
# 1- Load data
indicators_value = []
ticker_name = []
glob.glob("D:\Stock Study Excel Files\Input Excel Files\Stock USA\*.xlsx")
for f in glob.glob('D:\Stock Study Excel Files\Input Excel Files\Stock USA\*.xlsx'):
    df = pd.read_excel(f)
   # df.columns = map(str.capitalize, df.columns)
    #df.rename(columns={'Volume': 'Volume_BTC'}, inplace=True)
    tike = f.split('\\')[-1].split('.')[0]
    print(tike)
    df.insert(1, 'TICKER', tike)  # to bring excel file name
    # Clean nan values
    df = ta.utils.dropna(df)
    ####################################################################
    # 2-Add all ta features filling nans values (from Ta-Lib Except SuperTrend Because not in Ta-Lib)
    df = ta.add_all_ta_features(df, "Open", "High", "Low", "Close", "Volume_BTC", fillna=True)

    #####################################################################
    # 3- Calculate
    df['Signal'] = 0
    sell = []
    buy = []
    date_sell = []
    date_buy = []
    indicators = ['trend_psar']  # The indicators to be studied
    for indicator in indicators:
        # 3.1 Determine the Date of  first buy signal and then exit the loop
        for y in range(10, len(df.index)):
            if df[indicator].iloc[y] <= df['Close'].iloc[y] and (df[indicator].iloc[y - 1] > df['Close'].iloc[y - 1]):
                first_buy_signal = y
                break
        '''
        # 3.2 Beginning of the study of buying and selling signals from the day before the date of the first purchase signal 
        (identified from the previous step) to ensure that the study begins with a buy signal, not selling   '''

        for x in range(first_buy_signal - 1, len(df.index)):
            if df[indicator].iloc[x] >= df['Close'].iloc[x] and (df[indicator].iloc[x - 1] < df['Close'].iloc[x - 1]):
                df['Signal'].iloc[x] = 'Sell'
                sell.append(df['Close'].iloc[x])
                date_sell.append(df['Date'].iloc[x])
            elif df[indicator].iloc[x] <= df['Close'].iloc[x] and (df[indicator].iloc[x - 1] > df['Close'].iloc[x - 1]):
                df['Signal'].iloc[x] = 'Buy'
                buy.append(df['Close'].iloc[x])
                date_buy.append(df['Date'].iloc[x])
        print(len(buy))
        print(len(sell))
        ''' To avoid the presence of a buy signal at the end of operations without the presence of a buy signal, 
        therefore the two columns do not contain the same number and the accounts are stopped '''
        if len(buy) != len(sell):  # To avoid
            del buy[-1]
            del date_buy[-1]
        profits = pd.DataFrame()
        profits['Buy Price'] = buy
        profits['Buy Date'] = date_buy
        profits['Sell Price'] = sell
        profits['Sell Date'] = date_sell
        profits['Profits'] = ((profits['Sell Price'] - profits['Buy Price']) / profits['Buy Price']) * 100
        # profits.drop(profits.tail(1).index, inplace=True)  # drop last n rows
        sum(profits['Profits'])
        profits.round(2).to_excel(f'{f}.xlsx', sheet_name="indicator Osama", index=True, index_label="TICKER")
        indicators_value.append(sum(profits['Profits']))
    #########################################################################
    tik = df.iloc[0]['TICKER']
    ticker_name.append(tik)
dictionary = dict(zip(ticker_name, indicators_value))
basic = pd.DataFrame(indicators_value, ticker_name)
indicators_na = pd.DataFrame(indicators, index=[0])
final_results = pd.concat([indicators_na, basic], axis=0)
# final_results.insert(0, 'TICKER', tike)
final_results.round(2).to_excel('D:\Stock Study Excel Files\Output Excel Files\Stock USA\indicators.xlsx', sheet_name="indicators value",
                                index=True)
print(final_results)

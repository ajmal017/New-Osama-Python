import pandas as pd
import numpy as np
import ta
import glob
# Import Built-Ins
import logging

# Init Logging Facilities
log = logging.getLogger(__name__)
#################################################################
# 1- Load data
indicators_value = []
ticker_name = []
folder_path = "D:\Stock Study Excel Files\Input Excel Files\EGX\*.xls"
glob.glob(folder_path)
for f in glob.glob(folder_path):
    df = pd.read_excel(f, skiprows=1)
    df.columns = map(str.capitalize, df.columns)
    df.rename(columns={'Volume': 'Volume_BTC'}, inplace=True)
    tike = f.split('\\')[-1].split('.')[0]
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
    sell_date = []
    buy_date = []
    macd = 'trend_macd'
    mov = 'trend_macd_signal'
    indicators = ['MACD&MOV']  # The indicators to be studied
    # for indicator in indicators:
    # 3.1 Determine the Date of  first buy signal and then exit the loop
    for y in range(750, len(df.index)):
        if df[mov].iloc[y] <= df[macd].iloc[y] and (df[mov].iloc[y - 1] > df[macd].iloc[y - 1]):
            first_buy_signal = y
            break
    '''
    # 3.2 Beginning of the study of buying and selling signals from the day before the date of the first purchase signal 
    (identified from the previous step) to ensure that the study begins with a buy signal, not selling   '''

    for x in range(first_buy_signal - 1, len(df.index)):
        if df[mov].iloc[x] >= df[macd].iloc[x] and (df[mov].iloc[x - 1] < df[macd].iloc[x - 1]):
            df['Signal'].iloc[x] = 'Sell'
            sell.append(df['Close'].iloc[x])
            sell_date.append(df['Date'].iloc[x])
        elif df[mov].iloc[x] <= df[macd].iloc[x] and (df[mov].iloc[x - 1] > df[macd].iloc[x - 1]):
            df['Signal'].iloc[x] = 'Buy'
            buy.append(df['Close'].iloc[x])
            buy_date.append(df['Date'].iloc[x])
    ''' To avoid the presence of a buy signal at the end of operations without the presence of a buy signal, 
    therefore the two columns do not contain the same number and the accounts are stopped '''
    if len(buy) == (len(sell) + 1):  # to avoid the No. of signles not equal
        del buy[-1]
    del buy_date[-1]
    profits = pd.DataFrame()
    profits['Buy Price'] = buy
    profits['Buy Date'] = buy_date
    profits['Sell Price'] = sell
    profits['Sell Date'] = sell_date
    profits['Profits Percentage'] = ((profits['Sell Price'] - profits['Buy Price']) / profits['Buy Price']) * 100
    profits['Profits Value'] = (profits['Sell Price'] - profits['Buy Price'])
    indicators_value.append(sum(profits['Profits Percentage']))
    total_profits_value = sum(profits['Profits Value'])  # Total Profits Value With use indicator
    profits.loc['Total', 'Profits Percentage':'Profits Value'] = profits.sum(axis=0)
    profits.index = np.arange(1, len(profits) + 1)  # to make index start from 1
    # profits.round(2).to_excel(f'{f}.xlsx', sheet_name="indicator Osama", index=True, index_label="No")
    # print(f'the Buy and Sell Signels Export to Excel File at Folder({f}.xlsx')
    #########################################################################
    tik = df.iloc[0]['TICKER']
    ticker_name.append(tik)
    # We Must add eles here
    total_value = profits.iloc[len(buy) - 1]['Sell Price'] - profits.iloc[0]['Buy Price']  # Total Profits if Buy and Hold with any Trade
    total_value_per = (total_value / profits.iloc[0]['Buy Price']) * 100
    print(f'Tacker Name : {tike}')
    print(f'The Number of Buy Signales : {len(buy)}')
    print(f'The Number of sell signal : {len(sell)}')
    print(f'indicators Name : {macd, mov}')
    print(f'Total Profits Value With use indicator :{total_profits_value}', )
    print(f'Total Profits if Buy and Hold with no any Trade : {total_value}')
    d = {'Ticker Name': ticker_name, 'indi. Name': indicators, 'First Buy Price': profits.iloc[0]['Buy Price'], 'First Buy D': profits.iloc[0]['Buy Date'],
         'Last Sell Price': profits.iloc[len(buy) - 1]['Sell Price'], 'Last Sell D': profits.iloc[len(buy) - 1]['Sell Date'], 'Total Valu': total_profits_value,
         'Total. with indi Per %': indicators_value, 'Total Value if buy and hold': total_value, 'Total if Hold %': total_value_per}
    final_results = pd.DataFrame(d)
    final_results.index = np.arange(1, len(final_results) + 1)  # to make index start from 1
# final_results.round(2).to_excel('D:\Stock Study Excel Files\Output Excel Files\indicators.xlsx', sheet_name=tike, index=True, index_label="No.")
print(final_results)

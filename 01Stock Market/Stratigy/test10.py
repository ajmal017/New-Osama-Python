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
# Load data
indicators_value = []
ticker_name = []
glob.glob("D:\Stock Market\Daily\Test\*.xlsx")
for f in glob.glob('D:\Stock Market\Daily\Test\*.xlsx'):
    df = pd.read_excel(f)
    df.columns = map(str.capitalize, df.columns)


    def delete_row(self):


    # Instantiating a Workbook object by excel file path
    workbook = self.Workbook(self.dataDir + 'Book1.xls')

    # Accessing the first worksheet in the Excel file
    worksheet = workbook.getWorksheets().get(0)

    # Deleting 3rd row from the worksheet
    worksheet.getCells().deleteRows(2, 1, True)

    # Saving the modified Excel file in default (that is Excel 2003) format
    workbook.save(self.dataDir + "Delete Row.xls")

    print
    "Delete Row Successfully."
    # Clean nan values
    df = ta.utils.dropna(df)
    # Add all ta features filling nans values
    df = ta.add_all_ta_features(df, "Open", "High", "Low", "Close", "Volume_BTC", fillna=True)

######################################################################
    df['Signal'] = 0
    sell = []
    buy = []
    date_sell = []
    date_buy = []
    indicators = ['trend_psar']
    for indicator in indicators:
        for y in range(10, len(df.index)):
            if df[indicator].iloc[y] <= df['Close'].iloc[y] and (df[indicator].iloc[y - 1] > df['Close'].iloc[y - 1]):
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
        sum(profits['Profits'])
        indicators_value.append(sum(profits['Profits']))
    #####################################################################
    tik = df.iloc[0]['TICKER']
    ticker_name.append(tik)
dictionary = dict(zip(ticker_name, indicators_value))
basic = pd.DataFrame(indicators_value, ticker_name)
indicators_na = pd.DataFrame(indicators, index=[0])
final_results = pd.concat([indicators_na, basic], axis=0)
print(final_results.round(1))

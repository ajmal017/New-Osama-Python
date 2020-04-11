import talib
import pandas as pd
import ta
import glob
import matplotlib.pyplot as plt



# Load data
glob.glob("D:\Stock Market\Daily\Test\*.xlsx")
for f in glob.glob('D:\Stock Market\Daily\Test\*.xlsx'):
    df = pd.read_excel(f)
    # Clean nan values
    df = ta.utils.dropna(df)
    # Add all ta features filling nans values
    df = ta.add_all_ta_features(df, "Open", "High", "Low", "Close", "Volume_BTC", fillna=True)
    df[['trend_macd', 'trend_macd_signal']].tail(120).plot(figsize=(15, 15))
    plt.show()
    # Export to Excel File
    ##df.round(2).to_excel(f'{f}.xlsx', sheet_name="indicator Osama", index=False)
print('OK The Files Ready ')


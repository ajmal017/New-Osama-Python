#  all Indicators By TA-Lib
import talib
import pandas as pd
import ta
import glob

#  all Technical Analysis Features
# Load data
glob.glob("D:\Stock Market\Daily\Test\*.xlsx")
for f in glob.glob('D:\Stock Market\Daily\Test\*.xlsx'):
    df = pd.read_excel(f)
    # Clean nan values
    df = ta.utils.dropna(df)
    # Add all ta features filling nans values
    df = ta.add_all_ta_features(df, "Open", "High", "Low", "Close", "Volume_BTC", fillna=True)
    # Export to Excel File
    df.round(2).to_excel(f'{f}.xlsx', sheet_name="indicator Osama", index=False)
print('OK The Files Ready ')


# Example adding Particular Feature
"""
if you want Know function groups us:
talib.get_function_groups()

# Load datas
glob.glob("D:\Stock Market\Daily\Test\*.xlsx")
for f in glob.glob('D:\Stock Market\Daily\Test\*.xlsx'):
    df = pd.read_excel(f)
    # Clean nan values
    df = ta.utils.dropna(df)
    # Initialize Bollinger Bands Indicator
    indicator_bb = ta.volatility.BollingerBands(close=df["Close"], n=20, ndev=2)

    # Add Bollinger Bands features
    df['bb_bbm'] = indicator_bb.bollinger_mavg()
    df['bb_bbh'] = indicator_bb.bollinger_hband()
    df['bb_bbl'] = indicator_bb.bollinger_lband()

    # Add Bollinger Band high indicator
    df['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()

    # Add Bollinger Band low indicator
    df['bb_bbli'] = indicator_bb.bollinger_lband_indicator()

    # Add Width Size Bollinger Bands
    df['bb_bbw'] = indicator_bb.bollinger_wband()

    # Add Percentage Bollinger Bands
    df['bb_bbp'] = indicator_bb.bollinger_pband()
    # Export to Excel File
    df.round(2).to_excel(f'{f}.xlsx', sheet_name="indicator Osama", index=False)
    
print('OK The Files Ready ')
"""

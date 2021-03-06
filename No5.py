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
    # df.rename(columns={'Volume': 'Volume_BTC'}, inplace=True)
    tike = f.split('\\')[-1].split('.')[0]
    print(tike)
    df.insert(1, 'TICKER', tike)  # to bring excel file name
    # Clean nan values
    df = ta.utils.dropna(df)
    ####################################################################
    # 2-Add all ta features filling nans values (from Ta-Lib Except SuperTrend Because not in Ta-Lib)
    df = ta.add_all_ta_features(df, "Open", "High", "Low", "Close", "Volume_BTC", fillna=True)
    print(df)

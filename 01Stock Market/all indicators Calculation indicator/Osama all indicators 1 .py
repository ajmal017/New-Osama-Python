import pandas as pd
import ta

# Load datas
df = pd.read_csv('D:\datas.csv', sep=',')

# Clean NaN values
df = ta.utils.dropna(df)

# Add all ta features
df = ta.add_all_ta_features(
    df, open="Open", high="High", low="Low", close="Close", volume="Volume_BTC")
df.round(2).to_excel('D:\osama.xlsx', sheet_name="indicator Osama", index=False)
# vv Continue Post Processing vv

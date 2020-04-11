import pandas as pd

df = pd.read_excel('D:\Python\Project\EGX30.xlsx', sheet_name='EGX30')
df['H-L'] = df['high'] - df['low']
df['H-PC'] = abs(df['high'] - df['close'].shift(1))
df['L-PC'] = abs(df['low'] - df['close'].shift(1))
true_range = []
averag_true_range = []
atr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
upper_band_basic = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
"""
    SuperTrend Algorithm :

        BASIC UPPERBAND = (HIGH + LOW) / 2 + Multiplier * ATR
        BASIC LOWERBAND = (HIGH + LOW) / 2 - Multiplier * ATR

        FINAL UPPERBAND = IF( (Current BASICUPPERBAND < Previous FINAL UPPERBAND) or (Previous Close > Previous FINAL UPPERBAND))
                            THEN (Current BASIC UPPERBAND) ELSE Previous FINALUPPERBAND)
        FINAL LOWERBAND = IF( (Current BASIC LOWERBAND > Previous FINAL LOWERBAND) or (Previous Close < Previous FINAL LOWERBAND)) 
                            THEN (Current BASIC LOWERBAND) ELSE Previous FINAL LOWERBAND)

        SUPERTREND = IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close <= Current FINAL UPPERBAND)) THEN
                        Current FINAL UPPERBAND
                    ELSE
                        IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close > Current FINAL UPPERBAND)) THEN
                            Current FINAL LOWERBAND
                        ELSE
                            IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current Close >= Current FINAL LOWERBAND)) THEN
                                Current FINAL LOWERBAND
                            ELSE
                                IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current Close < Current FINAL LOWERBAND)) THEN
                                    Current FINAL UPPERBAND
    """

for x in range(0, len(df.index)):
    true_range2 = max(df['H-L'].iloc[x], df['H-PC'].iloc[x], df['L-PC'].iloc[x])
    true_range.append(true_range2)
df2 = pd.DataFrame(true_range, columns=['True Range'])
df['True Range'] = df2['True Range']
for x in range(2, len(df.index)):
    atr2 = df.loc[x:x + 9, "True Range"].mean()
    atr.append(atr2)
df3 = pd.DataFrame(atr, columns=['ATR'])
df['ATR'] = df3['ATR']
multiplier = 2
df['ubb'] = ((df['high'] + df['low']) / 2) + (df['ATR'] * multiplier)
df['lbb'] = ((df['high'] + df['low']) / 2) - (df['ATR'] * multiplier)
df['ubf'] = 0
df['lbf'] = 0
df['st'] = 0
for x in range(11, len(df.index)):
    if (df.loc[x, 'ubb'] < df.loc[x - 1, 'ubf']) or (df.loc[x - 1, 'close'] > df.loc[x - 1, 'ubf']):
        df.loc[x, 'ubf'] = df.loc[x, 'ubb']
    else:
        df.loc[x, 'ubf'] = df.loc[x - 1, 'ubf']
    if (df.loc[x, 'lbb'] > df.loc[x - 1, 'lbf']) or (df.loc[x - 1, 'close'] < df.loc[x - 1, 'lbf']):
        df.loc[x, 'lbf'] = df.loc[x, 'lbb']
    else:
        df.loc[x, 'lbf'] = df.loc[x - 1, 'lbf']
    if ((df.loc[x - 1, 'st'] == df.loc[x - 1, 'ubf']) and (df.loc[x, 'close'] <= df.loc[x, 'ubf'])) \
            or ((df.loc[x - 1, 'st'] == df.loc[x - 1, 'lbf']) and (df.loc[x, 'close'] <= df.loc[x, 'lbf'])):
        df.loc[x, 'st'] = df.loc[x, 'ubf']
    else:
        ((df.loc[x - 1, 'st'] == df.loc[x - 1, 'ubf']) and (df.loc[x, 'close'] > df.loc[x, 'ubf'])) \
        or ((df.loc[x - 1, 'st'] == df.loc[x - 1, 'lbf']) and (df.loc[x, 'close'] >= df.loc[x, 'lbf']))
        df.loc[x, 'st'] = df.loc[x, 'lbf']

df.round(2).to_excel(r'D:\Python\Project\Temp\osamapycharm.xlsx', sheet_name='EGX 30', index=False)

print(df.round(2))

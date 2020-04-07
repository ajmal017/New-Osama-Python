# The indicator calculates a group of files and extracts them into separate files
import pandas as pd
import glob

glob.glob("D:\Stock Market\Daily\Test\*.xls")
for f in glob.glob('D:\Stock Market\Daily\Test\*.xls'):
    df = pd.read_excel(f, skiprows=[0])
    df['H-L'] = df['HIGH'] - df['LOW']
    df['H-PC'] = abs(df['HIGH'] - df['CLOSE'].shift(1))
    df['L-PC'] = abs(df['LOW'] - df['CLOSE'].shift(1))
    averag_true_range = []
    atr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    upper_band_basic = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    """
            SuperTrend Algorithm :
        
                BASIC UPPERBAND = (HIGH + LOW) / 2 + Multiplier * ATR
                BASIC LOWERBAND = (HIGH + LOW) / 2 - Multiplier * ATR
        
                FINAL UPPERBAND = IF( (Current BASICUPPERBAND < Previous FINAL UPPERBAND) or (Previous CLOSE > Previous FINAL UPPERBAND))
                                    THEN (Current BASIC UPPERBAND) ELSE Previous FINALUPPERBAND)
                FINAL LOWERBAND = IF( (Current BASIC LOWERBAND > Previous FINAL LOWERBAND) or (Previous CLOSE < Previous FINAL LOWERBAND)) 
                                    THEN (Current BASIC LOWERBAND) ELSE Previous FINAL LOWERBAND)
        
                SUPERTREND = IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current CLOSE <= Current FINAL UPPERBAND)) THEN
                                Current FINAL UPPERBAND
                            ELSE
                                IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current CLOSE > Current FINAL UPPERBAND)) THEN
                                    Current FINAL LOWERBAND
                                ELSE
                                    IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current CLOSE >= Current FINAL LOWERBAND)) THEN
                                        Current FINAL LOWERBAND
                                    ELSE
                                        IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current CLOSE < Current FINAL LOWERBAND)) THEN
                                            Current FINAL UPPERBAND
            """
    df['True Range'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    period = 10
    for x in range(period, len(df.index)):
        atr2 = df.loc[x - 8:x + 1, "True Range"].mean()
        atr.append(atr2)
    df3 = pd.DataFrame(atr, columns=['ATR'])
    df['ATR'] = df3['ATR']
    multiplier = 3
    df['ubb'] = ((df['HIGH'] + df['LOW']) / 2) + (df['ATR'] * multiplier)
    df['lbb'] = ((df['HIGH'] + df['LOW']) / 2) - (df['ATR'] * multiplier)
    df['ubf'] = 0
    df['lbf'] = 0
    df['st'] = 0
    for x in range(period + 1, len(df.index)):
        if (df.loc[x, 'ubb'] < df.loc[x - 1, 'ubf']) or (df.loc[x - 1, 'CLOSE'] > df.loc[x - 1, 'ubf']):
            df.loc[x, 'ubf'] = df.loc[x, 'ubb']
        else:
            df.loc[x, 'ubf'] = df.loc[x - 1, 'ubf']
        if (df.loc[x, 'lbb'] > df.loc[x - 1, 'lbf']) or (df.loc[x - 1, 'CLOSE'] < df.loc[x - 1, 'lbf']):
            df.loc[x, 'lbf'] = df.loc[x, 'lbb']
        else:
            df.loc[x, 'lbf'] = df.loc[x - 1, 'lbf']
        if ((df.loc[x - 1, 'st'] == df.loc[x - 1, 'ubf']) and (df.loc[x, 'CLOSE'] <= df.loc[x, 'ubf'])) \
                or ((df.loc[x - 1, 'st'] == df.loc[x - 1, 'lbf']) and (df.loc[x, 'CLOSE'] <= df.loc[x, 'lbf'])):
            df.loc[x, 'st'] = df.loc[x, 'ubf']
        else:
            ((df.loc[x - 1, 'st'] == df.loc[x - 1, 'ubf']) and (df.loc[x, 'CLOSE'] > df.loc[x, 'ubf'])) \
            or ((df.loc[x - 1, 'st'] == df.loc[x - 1, 'lbf']) and (df.loc[x, 'CLOSE'] >= df.loc[x, 'lbf']))
            df.loc[x, 'st'] = df.loc[x, 'lbf']
    df.round(2).to_excel(f'{f}.xlsx', sheet_name='indicator', index=False)
    # print(df.round(2))

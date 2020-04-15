# Import Built-Ins
import logging
# Import Third-Party
import pandas as pd
import numpy as np
import glob
# Import Homebrew
import talib
import talib as ta
import matplotlib.pyplot as plt

plt.style.use('bmh')
# Init Logging Facilities
log = logging.getLogger(__name__)


#############################################################################################################
#                                                                                        Important Indicators
# 1-Simple Moving average
def moving_average(df, n):
    """Calculate the moving average for the given data.

    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    MA = pd.Series(df['Close'].rolling(n, min_periods=n).mean(), name='MA_' + str(n))
    df = df.join(MA)
    return df


# 2- Exponential Moving Average
def EMA(df, base, target, period, alpha=False):
    """
    Function to compute Exponential Moving Average (EMA)

    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        base : String indicating the column name from which the EMA needs to be computed from
        target : String indicates the column name to which the computed data needs to be stored
        period : Integer indicates the period of computation in terms of number of candles
        alpha : Boolean if True indicates to use the formula for computing EMA using alpha (default is False)

    Returns :
        df : Pandas DataFrame with new column added with name 'target'
    """

    con = pd.concat([df[:period][base].rolling(window=period).mean(), df[period:][base]])

    if (alpha == True):
        # (1 - alpha) * previous_val + alpha * current_val where alpha = 1 / period
        df[target] = con.ewm(alpha=1 / period, adjust=False).mean()
    else:
        # ((current_val - previous_val) * coeff) + previous_val where coeff = 2 / (period + 1)
        df[target] = con.ewm(span=period, adjust=False).mean()

    df[target].fillna(0, inplace=True)
    return df


# 3- Average True Range (ATR)
def ATR(df, period, ohlc=['Open', 'High', 'Low', 'Close']):
    """
    Function to compute Average True Range (ATR)

    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        period : Integer indicates the period of computation in terms of number of candles
        ohlc: List defining OHLC Column names (default ['Open', 'High', 'Low', 'Close'])

    Returns :
        df : Pandas DataFrame with new columns added for
            True Range (TR)
            ATR (ATR_$period)
    """
    atr = 'ATR_' + str(period)

    # Compute true range only if it is not computed and stored earlier in the df
    if not 'TR' in df.columns:
        df['h-l'] = df[ohlc[1]] - df[ohlc[2]]
        df['h-yc'] = abs(df[ohlc[1]] - df[ohlc[3]].shift())
        df['l-yc'] = abs(df[ohlc[2]] - df[ohlc[3]].shift())

        df['TR'] = df[['h-l', 'h-yc', 'l-yc']].max(axis=1)

        df.drop(['h-l', 'h-yc', 'l-yc'], inplace=True, axis=1)

    # Compute EMA of true range using ATR formula after ignoring first row
    EMA(df, 'TR', atr, period, alpha=True)

    return df


# 4- SuperTrend
def SuperTrend(df, period, multiplier, ohlc=['Open', 'High', 'Low', 'Close']):
    """
    Function to compute SuperTrend

    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        period : Integer indicates the period of computation in terms of number of candles
        multiplier : Integer indicates value to multiply the ATR
        ohlc: List defining OHLC Column names (default ['Open', 'High', 'Low', 'Close'])

    Returns :
        df : Pandas DataFrame with new columns added for
            True Range (TR), ATR (ATR_$period)
            SuperTrend (ST_$period_$multiplier)
            SuperTrend Direction (STX_$period_$multiplier)
    """

    ATR(df, period, ohlc=ohlc)
    atr = 'ATR_' + str(period)
    st = 'ST_' + str(period) + '_' + str(multiplier)
    stx = 'STX_' + str(period) + '_' + str(multiplier)

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

    # Compute basic upper and lower bands
    df['basic_ub'] = (df[ohlc[1]] + df[ohlc[2]]) / 2 + multiplier * df[atr]
    df['basic_lb'] = (df[ohlc[1]] + df[ohlc[2]]) / 2 - multiplier * df[atr]

    # Compute final upper and lower bands
    df['final_ub'] = 0.00
    df['final_lb'] = 0.00
    for i in range(period, len(df)):
        df['final_ub'].iat[i] = df['basic_ub'].iat[i] if df['basic_ub'].iat[i] < df['final_ub'].iat[i - 1] or df[ohlc[3]].iat[i - 1] > df['final_ub'].iat[i - 1] else df['final_ub'].iat[i - 1]
        df['final_lb'].iat[i] = df['basic_lb'].iat[i] if df['basic_lb'].iat[i] > df['final_lb'].iat[i - 1] or df[ohlc[3]].iat[i - 1] < df['final_lb'].iat[i - 1] else df['final_lb'].iat[i - 1]

    # Set the Supertrend value
    df[st] = 0.00
    for i in range(period, len(df)):
        df[st].iat[i] = df['final_ub'].iat[i] if df[st].iat[i - 1] == df['final_ub'].iat[i - 1] and df[ohlc[3]].iat[i] <= df['final_ub'].iat[i] else \
            df['final_lb'].iat[i] if df[st].iat[i - 1] == df['final_ub'].iat[i - 1] and df[ohlc[3]].iat[i] > df['final_ub'].iat[i] else \
                df['final_lb'].iat[i] if df[st].iat[i - 1] == df['final_lb'].iat[i - 1] and df[ohlc[3]].iat[i] >= df['final_lb'].iat[i] else \
                    df['final_ub'].iat[i] if df[st].iat[i - 1] == df['final_lb'].iat[i - 1] and df[ohlc[3]].iat[i] < df['final_lb'].iat[i] else 0.00

        # Mark the trend direction up/down
    df[stx] = np.where((df[st] > 0.00), np.where((df[ohlc[3]] < df[st]), 'down', 'up'), np.NaN)

    # Remove basic and final bands from the columns
    df.drop(['basic_ub', 'basic_lb', 'final_ub', 'final_lb'], inplace=True, axis=1)

    df.fillna(0, inplace=True)

    return df


# 5- Parabolic Sar
def parabolicsar(df):
    df['SAR'] = talib.SAR(df.High, df.Low, acceleration=0.02, maximum=0.2)
    return df


# 6- MACD
def MACD(df, fastEMA=12, slowEMA=26, signal=9, base='Close'):
    """
    Function to compute Moving Average Convergence Divergence (MACD)

    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        fastEMA : Integer indicates faster EMA
        slowEMA : Integer indicates slower EMA
        signal : Integer indicates the signal generator for MACD
        base : String indicating the column name from which the MACD needs to be computed from (Default Close)

    Returns :
        df : Pandas DataFrame with new columns added for
            Fast EMA (ema_$fastEMA)
            Slow EMA (ema_$slowEMA)
            MACD (macd_$fastEMA_$slowEMA_$signal)
            MACD Signal (signal_$fastEMA_$slowEMA_$signal)
            MACD Histogram (MACD (hist_$fastEMA_$slowEMA_$signal))
    """

    fE = "ema_" + str(fastEMA)
    sE = "ema_" + str(slowEMA)
    macd = "macd_" + str(fastEMA) + "_" + str(slowEMA) + "_" + str(signal)
    sig = "signal_" + str(fastEMA) + "_" + str(slowEMA) + "_" + str(signal)
    hist = "hist_" + str(fastEMA) + "_" + str(slowEMA) + "_" + str(signal)

    # Compute fast and slow EMA
    EMA(df, base, fE, fastEMA)
    EMA(df, base, sE, slowEMA)

    # Compute MACD
    df[macd] = np.where(np.logical_and(np.logical_not(df[fE] == 0), np.logical_not(df[sE] == 0)), df[fE] - df[sE], 0)

    # Compute MACD Signal
    EMA(df, macd, sig, signal)

    # Compute MACD Histogram
    df[hist] = np.where(np.logical_and(np.logical_not(df[macd] == 0), np.logical_not(df[sig] == 0)), df[macd] - df[sig], 0)

    return df


# 7-Bollinger Band (BBand)
def BBand(df, base='Close', period=20, multiplier=2):
    """
    Function to compute Bollinger Band (BBand)

    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        base : String indicating the column name from which the MACD needs to be computed from (Default Close)
        period : Integer indicates the period of computation in terms of number of candles
        multiplier : Integer indicates value to multiply the SD

    Returns :
        df : Pandas DataFrame with new columns added for
            Upper Band (UpperBB_$period_$multiplier)
            Lower Band (LowerBB_$period_$multiplier)
    """

    upper = 'UpperBB_' + str(period) + '_' + str(multiplier)
    lower = 'LowerBB_' + str(period) + '_' + str(multiplier)

    sma = df[base].rolling(window=period, min_periods=period - 1).mean()
    sd = df[base].rolling(window=period).std()
    df[upper] = sma + (multiplier * sd)
    df[lower] = sma - (multiplier * sd)

    df[upper].fillna(0, inplace=True)
    df[lower].fillna(0, inplace=True)

    return df


# 8- Relative Strength Index (RSI)
def RSI(df, base="Close", period=21):
    """
    Function to compute Relative Strength Index (RSI)

    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        base : String indicating the column name from which the MACD needs to be computed from (Default Close)
        period : Integer indicates the period of computation in terms of number of candles

    Returns :
        df : Pandas DataFrame with new columns added for
            Relative Strength Index (RSI_$period)
    """

    delta = df[base].diff()
    up, down = delta.copy(), delta.copy()

    up[up < 0] = 0
    down[down > 0] = 0

    rUp = up.ewm(com=period - 1, adjust=False).mean()
    rDown = down.ewm(com=period - 1, adjust=False).mean().abs()

    df['RSI_' + str(period)] = 100 - 100 / (1 + rUp / rDown)
    df['RSI_' + str(period)].fillna(0, inplace=True)

    return df


# 9-Commodity Channel Index(CCI)
def commodity_channel_index(df, n):
    """Calculate Commodity Channel Index for given data.

    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    PP = (df['High'] + df['Low'] + df['Close']) / 3
    CCI = pd.Series((PP - PP.rolling(n, min_periods=n).mean()) / PP.rolling(n, min_periods=n).std(),
                    name='CCI_' + str(n))
    df = df.join(CCI)
    return df


# 10- stochastic oscillator %K
def stochastic_oscillator_k(df):
    """Calculate stochastic oscillator %K for given data.

    :param df: pandas.DataFrame
    :return: pandas.DataFrame
    """
    SOk = pd.Series((df['Close'] - df['Low']) / (df['High'] - df['Low']), name='SO%k')
    df = df.join(SOk)
    return df


# 11-stochastic oscillator %D
def stochastic_oscillator_d(df, n):
    """Calculate stochastic oscillator %D for given data.
    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    SOk = pd.Series((df['Close'] - df['Low']) / (df['High'] - df['Low']), name='SO%k')
    SOd = pd.Series(SOk.ewm(span=n, min_periods=n).mean(), name='SO%d_' + str(n))
    df = df.join(SOd)
    return df


# 12-Pivot Points, Supports and Resistances
def ppsr(df):
    """Calculate Pivot Points, Supports and Resistances for given data

    :param df: pandas.DataFrame
    :return: pandas.DataFrame
    """
    PP = pd.Series((df['High'] + df['Low'] + df['Close']) / 3)
    R1 = pd.Series(2 * PP - df['Low'])
    S1 = pd.Series(2 * PP - df['High'])
    R2 = pd.Series(PP + df['High'] - df['Low'])
    S2 = pd.Series(PP - df['High'] + df['Low'])
    R3 = pd.Series(df['High'] + 2 * (PP - df['Low']))
    S3 = pd.Series(df['Low'] - 2 * (df['High'] - PP))
    psr = {'PP': PP, 'R1': R1, 'S1': S1, 'R2': R2, 'S2': S2, 'R3': R3, 'S3': S3}
    PSR = pd.DataFrame(psr)
    df = df.join(PSR)
    return df


#############################################################################################################
# Load Data
folder_path = "D:\*.xls"
glob.glob(folder_path)
for f in glob.glob(folder_path):
    df = pd.read_excel(f, skiprows=1)
    df.columns = map(str.capitalize, df.columns)
    df.rename(columns={'Volume': 'Volume_BTC'}, inplace=True)
    tike = f.split('\\')[-1].split('.')[0]
    df.insert(1, 'TICKER', tike)  # to bring excel file name
    ############################################################################################################
    # 3- Colacte Indicator Value
    indicators_check = [parabolicsar(df), SuperTrend(df, 10, 3)]
    for indicator in indicators_check:
        df = pd.merge(df, indicator)
    print(df.round(2).tail(5))

    ############################################################################################################
    # 4 -Indicators Study
    # 4.1- Parabolic SAR & SuperTrend Study
    df['Signal'] = 0
    indi_name = []
    sell = []
    buy = []
    sell_date = []
    buy_date = []
    ticker_name = []
    first_buy_price = []
    first_buy_date = []
    last_sell_price = []
    last_sell_date = []
    total_profits_value = []
    total_profits_per = []
    total_value_if_buy_and_hold = []
    total_if_hold_per = []
    indicators = ['SAR', 'ST_10_3']
    for indicator in indicators:
        # 4.1.1 Determine the Date of  first buy signal and then exit the loop
        for y in range(750, len(df.index)):
            if df[indicator].iloc[y] <= df['Close'].iloc[y] and (df[indicator].iloc[y - 1] > df['Close'].iloc[y - 1]):
                first_buy_signal = y
                print(y)
                break

        '''
        # 3.2 Beginning of the study of buying and selling signals from the day before the date of the first purchase signal 
        (identified from the previous step) to ensure that the study begins with a buy signal, not selling   '''
        for x in range(first_buy_signal - 1, len(df.index)):
            if df[indicator].iloc[x] >= df['Close'].iloc[x] and (df[indicator].iloc[x - 1] < df['Close'].iloc[x - 1]):
                df['Signal'].iloc[x] = 'Sell'
                sell.append(df['Close'].iloc[x])
                sell_date.append(df['Date'].iloc[x])
            elif df[indicator].iloc[x] <= df['Close'].iloc[x] and (df[indicator].iloc[x - 1] > df['Close'].iloc[x - 1]):
                df['Signal'].iloc[x] = 'Buy'
                buy.append(df['Close'].iloc[x])
                buy_date.append(df['Date'].iloc[x])
        print(len(buy))
        print(len(sell))

        ''' To avoid the presence of a buy signal at the end of operations without the presence of a buy signal, 
            therefore the two columns do not contain the same number and the accounts are stopped '''
        if len(buy) == (len(sell) + 1):  # to avoid the No. of signles not equal
            del buy[-1]
            del buy_date[-1]

        print(len(buy))
        print(len(sell))
        ##########################################################################################################
        profits = pd.DataFrame()
        profits['Buy Price'] = buy
        profits['Buy Date'] = buy_date
        profits['Sell Price'] = sell
        profits['Sell Date'] = sell_date
        profits['Profits Percentage'] = ((profits['Sell Price'] - profits['Buy Price']) / profits['Buy Price']) * 100
        profits['Profits Value'] = (profits['Sell Price'] - profits['Buy Price'])
        #indicators_value_per = sum(profits['Profits Percentage'])
        # sum(profits['Profits Value'])  # Total Profits Value With use indicator
        # indicators_value = profits.loc['Total', 'Profits Percentage':'Profits Value'] = profits.sum(axis=0)
        profits.index = np.arange(1, len(profits) + 1)  # to make index start from 1
        profits.round(2).to_excel(f'{f}.xlsx', sheet_name="indicator Osama", index=True, index_label="No")
        print(f'the Buy and Sell Signels Export to Excel File at Folder({f}.xlsx')
        print(profits.round(2).tail(5))

        #########################################################################
        tik = df.iloc[0]['TICKER']
        ticker_name.append(tik)
        indi_name.append(indicator)
        first_buy_price.append(profits.iloc[0]['Buy Price'])
        first_buy_date.append(profits.iloc[0]['Buy Date'])
        last_sell_price.append(profits.iloc[len(buy) - 1]['Sell Price'])
        last_sell_date.append(profits.iloc[len(buy) - 1]['Sell Date'])
        total_profits_value.append(sum(profits['Profits Value']))
        total_profits_per.append(((sum(profits['Profits Value'])-profits.iloc[0]['Buy Price'])/profits.iloc[0]['Buy Price'])*100)

        # We Must add eles here
        # total_value = profits.iloc[len(buy) - 1]['Sell Price'] - profits.iloc[0]['Buy Price']  # Total Profits if Buy and Hold with any Trade
        total_value_if_buy_and_hold.append(profits.iloc[len(buy) - 1]['Sell Price'] - profits.iloc[0]['Buy Price'])
        # total_value_per = (profits.iloc[len(buy) - 1]['Sell Price'] - profits.iloc[0]['Buy Price'] / profits.iloc[0]['Buy Price']) * 100
        total_if_hold_per.append(((profits.iloc[len(buy) - 1]['Sell Price'] - profits.iloc[0]['Buy Price']) / (profits.iloc[0]['Buy Price'])) * 100)

        # print(f'Tacker Name : {tike}')
        # print(f'The Number of Buy Signales : {len(buy)}')
        # print(f'The Number of sell signal : {len(sell)}')
        # print(f'indicators Name : {indicators}')
        # print(f'Total Profits Value With use indicator :{indicators_value}' )
        # print(f'Total Profits if Buy and Hold with no any Trade : {total_value}')
        d = {'Ticker Name': ticker_name, 'indi. Name': indi_name, 'First Buy Price': first_buy_price, 'First Buy D': first_buy_date, 'Last Sell Price': last_sell_price
            , 'Last Sell D': last_sell_date, 'Profits Value': total_profits_value, 'Profits Per %': total_profits_per, 'Total Value if buy and hold': total_value_if_buy_and_hold, 'Total if Hold %': total_if_hold_per}

        final_results = pd.DataFrame(d)
        # final_results.index = np.arange(1, len(final_results) + 1)  # to make index start from 1
    # final_results.round(2).to_excel('D:\Stock Study Excel Files\Output Excel Files\indicators.xlsx', sheet_name=tike, index=True, index_label="No.")
print(final_results.round(2).tail(10))

############################################################################################################

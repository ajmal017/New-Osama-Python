def EMA(dfst, base, target, period, alpha=False):
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

    con = pd.concat([dfst[:period][base].rolling(window=period).mean(), dfst[period:][base]])

    if (alpha == True):
        # (1 - alpha) * previous_val + alpha * current_val where alpha = 1 / period
        dfst[target] = con.ewm(alpha=1 / period, adjust=False).mean()
    else:
        # ((current_val - previous_val) * coeff) + previous_val where coeff = 2 / (period + 1)
        dfst[target] = con.ewm(span=period, adjust=False).mean()

    dfst[target].fillna(0, inplace=True)
    return dfst


def ATR(dfst, period, ohlc=['Open', 'High', 'Low', 'Close']):
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
    if not 'TR' in dfst.columns:
        dfst['h-l'] = dfst[ohlc[1]] - dfst[ohlc[2]]
        dfst['h-yc'] = abs(dfst[ohlc[1]] - dfst[ohlc[3]].shift())
        dfst['l-yc'] = abs(dfst[ohlc[2]] - dfst[ohlc[3]].shift())

        dfst['TR'] = dfst[['h-l', 'h-yc', 'l-yc']].max(axis=1)

        dfst.drop(['h-l', 'h-yc', 'l-yc'], inplace=True, axis=1)

    # Compute EMA of true range using ATR formula after ignoring first row
    EMA(dfst, 'TR', atr, period, alpha=True)

    return dfst


def SuperTrend(dfst, period, multiplier, ohlc=['Open', 'High', 'Low', 'Close']):
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

    ATR(dfst, period, ohlc=ohlc)
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
    dfst['basic_ub'] = (dfst[ohlc[1]] + dfst[ohlc[2]]) / 2 + multiplier * dfst[atr]
    dfst['basic_lb'] = (dfst[ohlc[1]] + dfst[ohlc[2]]) / 2 - multiplier * dfst[atr]

    # Compute final upper and lower bands
    dfst['final_ub'] = 0.00
    dfst['final_lb'] = 0.00
    for i in range(period, len(dfst)):
        dfst['final_ub'].iat[i] = dfst['basic_ub'].iat[i] if dfst['basic_ub'].iat[i] < dfst['final_ub'].iat[i - 1] or dfst[ohlc[3]].iat[i - 1] > dfst['final_ub'].iat[i - 1] else dfst['final_ub'].iat[i - 1]
        dfst['final_lb'].iat[i] = dfst['basic_lb'].iat[i] if dfst['basic_lb'].iat[i] > dfst['final_lb'].iat[i - 1] or dfst[ohlc[3]].iat[i - 1] < dfst['final_lb'].iat[i - 1] else dfst['final_lb'].iat[i - 1]

    # Set the Supertrend value
    dfst[st] = 0.00
    for i in range(period, len(dfst)):
        dfst[st].iat[i] = dfst['final_ub'].iat[i] if dfst[st].iat[i - 1] == dfst['final_ub'].iat[i - 1] and dfst[ohlc[3]].iat[i] <= dfst['final_ub'].iat[i] else \
            dfst['final_lb'].iat[i] if dfst[st].iat[i - 1] == dfst['final_ub'].iat[i - 1] and dfst[ohlc[3]].iat[i] > dfst['final_ub'].iat[i] else \
                dfst['final_lb'].iat[i] if dfst[st].iat[i - 1] == dfst['final_lb'].iat[i - 1] and dfst[ohlc[3]].iat[i] >= dfst['final_lb'].iat[i] else \
                    dfst['final_ub'].iat[i] if dfst[st].iat[i - 1] == dfst['final_lb'].iat[i - 1] and dfst[ohlc[3]].iat[i] < dfst['final_lb'].iat[i] else 0.00

        # Mark the trend direction up/down
    dfst[stx] = np.where((dfst[st] > 0.00), np.where((dfst[ohlc[3]] < dfst[st]), 'down', 'up'), np.NaN)

    # Remove basic and final bands from the columns
    dfst.drop(['basic_ub', 'basic_lb', 'final_ub', 'final_lb'], inplace=True, axis=1)

    dfst.fillna(0, inplace=True)

    return dfst


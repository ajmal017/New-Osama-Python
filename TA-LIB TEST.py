
from __future__ import division
from functools import wraps
import numpy as np
from pandas import DataFrame, Series

import pandas as pd


def sar(s, af=0.02, amax=0.2):
    high, low = s.High, s.Low

    # Starting values
    sig0, xpt0, af0 = True, high[0], af
    sar = [low[0] - (high - low).std()]

    for i in range(1, len(s)):
        sig1, xpt1, af1 = sig0, xpt0, af0

        lmin = min(low[i - 1], low[i])
        lmax = max(high[i - 1], high[i])

        if sig1:
            sig0 = low[i] > sar[-1]
            xpt0 = max(lmax, xpt1)
        else:
            sig0 = high[i] >= sar[-1]
            xpt0 = min(lmin, xpt1)

        if sig0 == sig1:
            sari = sar[-1] + (xpt1 - sar[-1]) * af1
            af0 = min(amax, af1 + af)

            if sig0:
                af0 = af0 if xpt0 > xpt1 else af1
                sari = min(sari, lmin)
            else:
                af0 = af0 if xpt0 < xpt1 else af1
                sari = max(sari, lmax)
        else:
            af0 = af
            sari = xpt0

        sar.append(sari)

    return Series(sar, index=s.index)

s=pd.read_excel("D:\Stock Market\Daily\Test\EGX30C.xlsx")
print(sar(s, af=0.02, amax=0.2))

If((Cross(MACD() ,Mov(MACD(),25,E))) and (Ref(MACD() , -1) < ref(Mov(MACD(),25,E), -1)), 1, 0)
If((Cross(C, FmlVar("Supertrend", "ST")) AND ((Ref(C, -1) < Ref(FmlVar("Supertrend", "ST"),-1)), 1, 0))
Cross(MACD() ,Mov(MACD(),25,E)
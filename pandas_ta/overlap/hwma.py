# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta.utils import get_offset, verify_series


def hwma(close, na=None, nb=None, nc=None, offset=None, **kwargs):
    """Indicator: Holt-Winter Moving Average"""
    # Validate Arguments
    close = verify_series(close)
    na = float(na) if na and na > 0 else 0.2
    nb = float(nb) if nb and nb > 0 else 0.1
    nc = float(nc) if nc and nc > 0 else 0.1
    offset = get_offset(offset)

    # Initialize ..
    m = close.size
    last_f = close[0]
    # last_a, last_v = 0, 0
    last_a = last_v = 0
    result = []

    # Calculate ..
    for i in range(m):
        F = (1.0 - na) * (last_f + last_v + 0.5 * last_a) + na * close[i]
        V = (1.0 - nb) * (last_v + last_a) + nb * (F - last_f)
        A = (1.0 - nc) * last_a + nc * (V - last_v)
        result.append((F + V + 0.5 * A))
        # update values
        last_a, last_f, last_v = A, F, V

    hwma = Series(result, index=close.index)

    # Offset
    if offset != 0:
        hwma = hwma.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        hwma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        hwma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name & Category
    suffix = f"{na}_{nb}_{nc}"
    hwma.name = f"HWMA_{suffix}"
    hwma.category = "overlap"

    return hwma



hwma.__doc__ = \
"""HWMA (Holt-Winter Moving Average)

Indicator HWMA (Holt-Winter Moving Average) is a three-parameter moving average
by the Holt-Winter method; the three parameters should be selected to obtain a
forecast.

This version has been implemented for Pandas TA by rengel8 based
on a publication for MetaTrader 5.

Sources:
    https://www.mql5.com/en/code/20856

Calculation:
    HWMA[i] = F[i] + V[i] + 0.5 * A[i]
    where..
    F[i] = (1-na) * (F[i-1] + V[i-1] + 0.5 * A[i-1]) + na * Price[i]
    V[i] = (1-nb) * (V[i-1] + A[i-1]) + nb * (F[i] - F[i-1])
    A[i] = (1-nc) * A[i-1] + nc * (V[i] - V[i-1])

Args:
    na - parameter of the equation that describes a smoothed series (from 0 to 1)
    nb - parameter of the equation to assess the trend (from 0 to 1)
    nc - parameter of the equation to assess seasonality (from 0 to 1)
    close (pd.Series): Series of 'close's

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: hwma
"""
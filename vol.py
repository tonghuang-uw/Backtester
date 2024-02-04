import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def robust_vol_cal(
    daily_returns: pd.Series,
    days: int = 35,
    min_periods: int = 10,
    vol_abs_min: float = 0.0000000001,
    vol_floor: bool = True,
    floor_min_quant: float = 0.05,
    floor_min_periods: int = 100,
    floor_days: int = 500,
    backfill: bool = False,
    **ignored_kwargs,
) -> pd.Series:
    """
    Robust exponential volatility calculation, assuming daily series of prices
    We apply an absolute minimum level of vol (absmin);
    and a volfloor based on lowest vol over recent history

    :param x: data
    :type x: Tx1 pd.Series

    :param days: Number of days in lookback (*default* 35)
    :type days: int

    :param min_periods: The minimum number of observations (*default* 10)
    :type min_periods: int

    :param vol_abs_min: The size of absolute minimum (*default* =0.0000000001)
      0.0= not used
    :type absmin: float or None

    :param vol_floor Apply a floor to volatility (*default* True)
    :type vol_floor: bool

    :param floor_min_quant: The quantile to use for volatility floor (eg 0.05
      means we use 5% vol) (*default 0.05)
    :type floor_min_quant: float

    :param floor_days: The lookback for calculating volatility floor, in days
      (*default* 500)
    :type floor_days: int

    :param floor_min_periods: Minimum observations for floor - until reached
      floor is zero (*default* 100)
    :type floor_min_periods: int

    :returns: pd.DataFrame -- volatility measure
    """
    # Standard deviation will be nan for first 10 non nan values
    vol = simple_ewvol_cal(daily_returns, days=days, min_periods=min_periods)
    vol = apply_min_floor(vol, vol_abs_min=vol_abs_min)

    if vol_floor:
        vol = apply_vol_floor(
            vol,
            floor_min_quant=floor_min_quant,
            floor_min_period=floor_min_periods,
            floor_days=floor_days,
        )

    if backfill:
        # use the first vol in the past, sort of cheating
        vol = backfill_vol(vol)

    return vol


def apply_min_floor(
    vol: pd.Series,
    vol_abs_min: float = 0.0000000001
) -> pd.Series:
    # return vol min if vol is smaller
    vol[vol<vol_abs_min] = vol_abs_min

    return vol

def apply_vol_floor(
    vol: pd.Series,
    floor_min_quant: float = 0.05,
    floor_min_period: int = 100,
    floor_days: int = 500,
) -> pd.Series:
    # Find the minimum quantile to set as the minimum
    vol_min = vol.rolling(min_periods=floor_min_period, window = floor_days).quantile(
        q = floor_min_quant
    )
    return vol_min


def backfill_vol(vol: pd.Series) -> pd.Series:
    # have to fill forwards first, as it's only the start we want to
    # backfill, eg before any value available

    vol_forward_fill = vol.fillna(method = 'ffill')
    vol_backward_fill = vol.fillna(method = 'bfill')

    return vol_backward_fill

def simple_ewvol_cal(
    daily_return: pd.Series,
    days: int = 25,
    min_periods = 10
) -> pd.Series:

    # Standard deviation will be nan for first 10 non nan values
    vol = daily_return.ewm(adjust = True, span = days, min_periods = min_periods).std()

    return vol


def simple_vol_cal(
    daily_return: pd.Series,
    days: int = 25,
    min_periods = 10
) -> pd.Series:

    # Standard deviation will be nan for first 10 non nan values
    vol = daily_return.rolling(days, min_periods = min_periods).std()

    return vol

  # For reproducibility
# Generate 100 days of synthetic daily returns
np.random.seed(100)
daily_returns = pd.Series(np.random.normal(0, 0.025, 3000), index=pd.date_range(start='2015-01-01', periods=3000))
price = (1 + daily_returns).cumprod()

vol = robust_vol_cal(daily_returns)

fast_ma = price.rolling(25, min_periods=10).mean()
slow_ma = price.rolling(64, min_periods=10).mean()
raw_ma = fast_ma - slow_ma
forecast = (raw_ma/vol).clip(lower = -20, upper = 20)

plt.figure(figsize= (10,7))
plt.subplot(3, 1, 1)
daily_returns.plot(title = 'daily return')

plt.subplot(3, 1, 2)
price.plot(title = 'price')

plt.subplot(3, 1, 3)
forecast.plot(title = 'vol')
plt.show()
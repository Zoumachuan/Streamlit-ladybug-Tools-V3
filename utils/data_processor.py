# data_processor.py

import pandas as pd
import numpy as np
from ladybug.analysisperiod import AnalysisPeriod

def filter_by_analysis_period(data, period):
    """
    根据分析周期筛选数据。

    Args:
        data (TimeSeries): 要筛选的时间序列数据。
        period (AnalysisPeriod): 分析周期。

    Returns:
        TimeSeries: 筛选后的时间序列数据。
    """
    return data.filter_by_analysis_period(period)

def calculate_monthly_averages(data, datetimes):
    """
    计算月平均值。

    Args:
        data (list): 数据值列表。
        datetimes (list): 数据对应的日期时间列表。

    Returns:
        pandas.Series: 每月的平均值。
    """
    df = pd.DataFrame({"data": data})
    df["Month"] = pd.to_datetime(datetimes).month
    return df.groupby("Month")["data"].mean()

def calculate_daily_averages(data, datetimes):
    """
    计算日平均值。

    Args:
        data (list): 数据值列表。
        datetimes (list): 数据对应的日期时间列表。

    Returns:
        pandas.Series: 每日的平均值。
    """
    df = pd.DataFrame({"data": data})
    df["Day"] = pd.to_datetime(datetimes).dayofyear
    return df.groupby("Day")["data"].mean()

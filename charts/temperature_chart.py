# temperature_chart.py

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils.chart_generator import generate_bar_chart
from utils.data_processor import filter_by_analysis_period, calculate_daily_averages, calculate_monthly_averages
from utils.template_base import map_to_color
from utils.openai_integration import generate_temperature_analysis_advice
from ladybug.analysisperiod import AnalysisPeriod

def generate_temperature_charts(epw, start_month, end_month, color_scheme):
    """
    生成温度相关图表。

    Args:
        epw (EPW): 加载的EPW对象。
        start_month (int): 起始月份。
        end_month (int): 终止月份。
        color_scheme (int): 色卡编号。
    """
    # 创建分析周期
    range_select = AnalysisPeriod(st_month=start_month, end_month=end_month)
    range_full = AnalysisPeriod(st_month=1, end_month=12)
    range_day = AnalysisPeriod(st_month=start_month, st_day=1, end_month=end_month, end_day=31)

    # 获取干球温度数据
    dry_bulb_temps_select = filter_by_analysis_period(epw.dry_bulb_temperature, range_select)
    dry_bulb_temps_full = filter_by_analysis_period(epw.dry_bulb_temperature, range_full)
    dry_bulb_temps_day = filter_by_analysis_period(epw.dry_bulb_temperature, range_day)
    
    temperature_values_select = dry_bulb_temps_select.values
    temperature_values_full = dry_bulb_temps_full.values
    temperature_values_day = dry_bulb_temps_day.values

    # 处理颜色映射
    min_temp_select = np.min(temperature_values_select)
    max_temp_select = np.max(temperature_values_select)
    min_temp_full = np.min(temperature_values_full)
    max_temp_full = np.max(temperature_values_full)

    color_values_select = [map_to_color(temp, min_temp_select, max_temp_select, color_scheme) for temp in temperature_values_select]
    color_values_full = [map_to_color(temp, min_temp_full, max_temp_full, color_scheme) for temp in temperature_values_full]
    
    # 生成每小时的干球温度柱状图
    fig_dry1 = generate_bar_chart(
        temperature_values_select,
        f"Hourly Dry Bulb Temperature ({start_month} to {end_month} Month)",
        "Hour",
        "Dry Bulb Temperature (°C)",
        color_values_select
    )
    
    # 计算日均温
    daily_averages = calculate_daily_averages(temperature_values_day, dry_bulb_temps_day.datetimes)
    min_temp_daily_avg = daily_averages.min()
    max_temp_daily_avg = daily_averages.max()
    color_values_day = [map_to_color(temp, min_temp_daily_avg, max_temp_daily_avg, color_scheme) for temp in daily_averages]

    # 生成每日的干球温度柱状图
    fig_dry2 = generate_bar_chart(
        daily_averages,
        f"Daily Dry Bulb Temperature ({start_month} to {end_month} Month)",
        "Day",
        "Daily Average Dry Bulb Temperature (°C)",
        color_values_day
    )

    # 计算每月的干球温度均值
    monthly_averages = calculate_monthly_averages(temperature_values_full, dry_bulb_temps_full.datetimes)
    min_avg_temp = monthly_averages.min()
    max_avg_temp = monthly_averages.max()
    avg_color_values = [map_to_color(temp, min_avg_temp, max_avg_temp, color_scheme) for temp in monthly_averages]
    
    # 生成每月的干球温度柱状图
    fig_dry3 = generate_bar_chart(
        monthly_averages,
        "Monthly Average Dry Bulb Temperature",
        "Month",
        "Average Dry Bulb Temperature (°C)",
        avg_color_values
    )
    fig_dry3.update_xaxes(tickvals=list(range(1, 13)), ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

    # 显示图表
    chart_selection = st.radio('Select Chart to Display', ['Hourly Dry Bulb Temperature', 'Daily Dry Bulb Temperature', 'Monthly Average Dry Bulb Temperature'])
    if chart_selection == 'Hourly Dry Bulb Temperature':
        st.plotly_chart(fig_dry1, use_container_width=True)
    elif chart_selection == 'Daily Dry Bulb Temperature':
        st.plotly_chart(fig_dry2, use_container_width=True)
    else:
        st.plotly_chart(fig_dry3, use_container_width=True)

    # 计算一些总结性统计数据
    total_avg_temp = monthly_averages.mean()
    coldest_month = monthly_averages.idxmin()
    hottest_month = monthly_averages.idxmax()
    temp_difference = max_avg_temp - min_avg_temp
    
    # 计算不同温度范围的月数
    extreme_cold_months = monthly_averages[(monthly_averages < -10)].shape[0]
    cold_months = monthly_averages[((monthly_averages >= -10) & (monthly_averages < 0))].shape[0]
    cool_months = monthly_averages[((monthly_averages >= 0) & (monthly_averages < 15))].shape[0]
    mild_months = monthly_averages[((monthly_averages >= 15) & (monthly_averages < 20))].shape[0]
    warm_months = monthly_averages[((monthly_averages >= 20) & (monthly_averages < 25))].shape[0]
    hot_months = monthly_averages[((monthly_averages >= 25) & (monthly_averages < 30))].shape[0]
    very_hot_months = monthly_averages[((monthly_averages >= 30) & (monthly_averages < 35))].shape[0]
    extreme_hot_months = monthly_averages[(monthly_averages >= 35)].shape[0]

    # 计算每日日均温的分布
    extreme_cold_days = daily_averages[(daily_averages < -30)].shape[0]
    very_cold_days = daily_averages[((daily_averages >= -30) & (daily_averages < -20))].shape[0]
    cold_days = daily_averages[((daily_averages >= -20) & (daily_averages < -10))].shape[0]
    cool_days = daily_averages[((daily_averages >= -10) & (daily_averages < 0))].shape[0]
    mild_days = daily_averages[((daily_averages >= 0) & (daily_averages < 10))].shape[0]
    moderate_days = daily_averages[((daily_averages >= 10) & (daily_averages < 20))].shape[0]
    warm_days = daily_averages[((daily_averages >= 20) & (daily_averages < 30))].shape[0]
    hot_days = daily_averages[((daily_averages >= 30) & (daily_averages < 40))].shape[0]
    extreme_hot_days = daily_averages[(daily_averages >= 40)].shape[0]

    monthly_text = str(
        f"从全年来看，总的平均温度是{total_avg_temp:.2f}°C，"
        f"最高温度出现在{hottest_month}月，为{monthly_averages.max():.2f}°C，"
        f"最低温度出现在{coldest_month}月，为{monthly_averages.min():.2f}°C，"
        f"最冷月与最暖月之间的温差为{temp_difference:.2f}°C，"
        f"极寒温度的月份数量为{extreme_cold_months}个月，寒冷温度的月份数量为{cold_months}个月"
        f"凉爽温度的月份数量为{cool_months}个月，温和温度的月份数量为{mild_months}个月，"
        f"温暖温度的月份数量为{warm_months}个月，炎热温度的月份数量为{hot_months}个月，十分炎热温度的月份数量为{very_hot_months}个月"
        f"极热温度的月份数量为{extreme_hot_months}个月"
    )

    daily_text = str(
        f"当前月份的平均温度是{daily_averages.mean():.2f}°C，"
        f"最高温度是{max_temp_daily_avg:.2f}°C，最低温度是{min_temp_daily_avg:.2f}°C，"
        f"极寒温度的天气有{extreme_cold_days}天，十分寒冷温度的天气有{very_cold_days}天，寒冷温度的天气有{cold_days}天，"
        f"冷温度的天气有{cool_days}天，凉爽温度的天气有{mild_days}天，"
        f"温和温度的天气有{moderate_days}天，温暖温度的天气有{warm_days}天，"
        f"炎热温度的天气有{hot_days}天，极热温度的天气有{extreme_hot_days}天"
    )

    # 新增AI分析按钮
    if st.button('Current Month and Annual Temperature Evaluation'):
        advice = generate_temperature_analysis_advice(monthly_text, daily_text)
        st.markdown(f"**AI分析结果:**\n{advice}")


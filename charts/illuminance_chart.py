# illuminance_chart.py

import streamlit as st
import numpy as np
from utils.chart_generator import generate_bar_chart
from utils.data_processor import filter_by_analysis_period, calculate_daily_averages, calculate_monthly_averages
from utils.template_base import map_to_color
from ladybug.analysisperiod import AnalysisPeriod

def generate_illuminance_charts(epw, start_month, end_month, color_scheme, ill_type):
    """
    生成照度相关图表。

    Args:
        epw (EPW): 加载的EPW对象。
        start_month (int): 起始月份。
        end_month (int): 终止月份。
        color_scheme (int): 色卡编号。
        ill_type (str): 照度类型（"Direct", "Diffuse", "Global"之一）。
    """
    # 创建分析周期
    range_select = AnalysisPeriod(st_month=start_month, end_month=end_month)
    range_full = AnalysisPeriod(st_month=1, end_month=12)
    range_day = AnalysisPeriod(st_month=start_month, st_day=1, end_month=end_month, end_day=31)

    # 根据照度类型选择数据
    if ill_type == "Direct":
        ill_select = filter_by_analysis_period(epw.direct_normal_illuminance, range_select)
        ill_full = filter_by_analysis_period(epw.direct_normal_illuminance, range_full)
        ill_day = filter_by_analysis_period(epw.direct_normal_illuminance, range_day)
        y_label = "Direct Normal Illuminance (lux)"
    elif ill_type == "Diffuse":
        ill_select = filter_by_analysis_period(epw.diffuse_horizontal_illuminance, range_select)
        ill_full = filter_by_analysis_period(epw.diffuse_horizontal_illuminance, range_full)
        ill_day = filter_by_analysis_period(epw.diffuse_horizontal_illuminance, range_day)
        y_label = "Diffuse Horizontal Illuminance (lux)"
    elif ill_type == "Global":
        ill_select = filter_by_analysis_period(epw.global_horizontal_illuminance, range_select)
        ill_full = filter_by_analysis_period(epw.global_horizontal_illuminance, range_full)
        ill_day = filter_by_analysis_period(epw.global_horizontal_illuminance, range_day)
        y_label = "Global Horizontal Illuminance (lux)"

    illuminance_values_select = ill_select.values
    illuminance_values_full = ill_full.values
    illuminance_values_day = ill_day.values

    # 处理颜色映射
    min_ill_select = np.min(illuminance_values_select)
    max_ill_select = np.max(illuminance_values_select)
    min_ill_full = np.min(illuminance_values_full)
    max_ill_full = np.max(illuminance_values_full)

    color_values_select = [map_to_color(ill, min_ill_select, max_ill_select, color_scheme) for ill in illuminance_values_select]
    color_values_full = [map_to_color(ill, min_ill_full, max_ill_full, color_scheme) for ill in illuminance_values_full]
    
    # 生成每小时的照度柱状图
    fig_ill1 = generate_bar_chart(
        illuminance_values_select,
        f"Hourly {y_label} ({start_month} to {end_month} Month)",
        "Hour",
        y_label,
        color_values_select
    )
    
    # 计算日均照度
    daily_averages_ill = calculate_daily_averages(illuminance_values_day, ill_day.datetimes)
    min_ill_daily_avg = daily_averages_ill.min()
    max_ill_daily_avg = daily_averages_ill.max()
    color_values_day_ill = [map_to_color(ill, min_ill_daily_avg, max_ill_daily_avg, color_scheme) for ill in daily_averages_ill]

    # 生成每日的照度柱状图
    fig_ill2 = generate_bar_chart(
        daily_averages_ill,
        f"Daily {y_label} ({start_month} to {end_month} Month)",
        "Day",
        f"Daily Average {y_label}",
        color_values_day_ill
    )

    # 计算每月的照度均值
    monthly_averages_ill = calculate_monthly_averages(illuminance_values_full, ill_full.datetimes)
    min_avg_ill = monthly_averages_ill.min()
    max_avg_ill = monthly_averages_ill.max()
    avg_color_values_ill = [map_to_color(ill, min_avg_ill, max_avg_ill, color_scheme) for ill in monthly_averages_ill]
    
    # 生成每月的照度柱状图
    fig_ill3 = generate_bar_chart(
        monthly_averages_ill,
        f"Monthly Average {y_label}",
        "Month",
        f"Average {y_label}",
        avg_color_values_ill
    )
    fig_ill3.update_xaxes(tickvals=list(range(1, 13)), ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

    # 显示图表
    chart_selection = st.radio('Select Chart to Display', ['Hourly Illuminance', 'Daily Illuminance', 'Monthly Average Illuminance'])
    if chart_selection == 'Hourly Illuminance':
        st.plotly_chart(fig_ill1, use_container_width=True)
    elif chart_selection == 'Daily Illuminance':
        st.plotly_chart(fig_ill2, use_container_width=True)
    else:
        st.plotly_chart(fig_ill3, use_container_width=True)

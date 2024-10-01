# wind_chart.py

import streamlit as st
import numpy as np
from utils.chart_generator import generate_bar_chart, generate_wind_rose
from utils.data_processor import filter_by_analysis_period, calculate_daily_averages, calculate_monthly_averages
from utils.template_base import map_to_color
from utils.openai_integration import generate_wind_analysis_advice
from ladybug.analysisperiod import AnalysisPeriod
from ladybug.windrose import WindRose

def generate_legend_parameters(color_scheme):
    """
    生成风玫瑰图的图例参数。

    Args:
        color_scheme (int): 色卡编号。

    Returns:
        LegendParameters: 风玫瑰图的图例参数。
    """
    from ladybug.legend import LegendParameters
    from ladybug.color import Color

    # 根据色卡编号选择颜色
    color_list = []
    if color_scheme == 1:
        color_list = [Color(0, 0, 0), Color(240, 240, 240)]
    elif color_scheme == 2:
        color_list = [Color(65, 65, 255), Color(255, 65, 65)]
    elif color_scheme == 3:
        color_list = [Color(238, 105, 131), Color(255, 245, 228)]
    elif color_scheme == 4:
        color_list = [Color(151, 92, 141), Color(255, 173, 188)]
    elif color_scheme == 5:
        color_list = [Color(34, 87, 126), Color(149, 209, 204)]
    elif color_scheme == 6:
        color_list = [Color(185, 255, 252), Color(117, 121, 231)]
    elif color_scheme == 7:
        color_list = [Color(26, 18, 11), Color(229, 229, 203)]
    elif color_scheme == 8:
        color_list = [Color(109, 159, 217), Color(238, 222, 236)]
    elif color_scheme == 9:
        color_list = [Color(45, 34, 78), Color(235, 211, 5)]  # 默认黑白颜色

    return LegendParameters(colors=color_list)

    return LegendParameters(colors=color_list)

def get_wind_direction_name(degrees):
    """
    将风向度数转换为可读的风向名称。

    Args:
        degrees (list): 风向度数列表。

    Returns:
        str: 风向名称。
    """
    directions = ["北", "北偏东", "东北", "东偏北",
                  "东", "东偏南", "东南", "南偏东",
                  "南", "南偏西", "西南", "西偏南",
                  "西", "西偏北", "西北", "北偏西"]
    degree_val = degrees[0]  # 获取列表中的第一个元素
    index = round((((degree_val + 11.25) % 360) - 11.25) / 22.5) 
    return directions[index % 16]

def generate_wind_charts(epw, start_month, end_month, color_scheme,show_charts=True):
    """
    生成风速和风玫瑰图。

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

    # 获取风速数据
    wind_speed_select = filter_by_analysis_period(epw.wind_speed, range_select)
    wind_speed_full = filter_by_analysis_period(epw.wind_speed, range_full)
    wind_speed_day = filter_by_analysis_period(epw.wind_speed, range_day)
    
    speed_values_select = wind_speed_select.values
    speed_values_full = wind_speed_full.values
    speed_values_day = wind_speed_day.values

    # 获取风向数据
    wind_direction_select = filter_by_analysis_period(epw.wind_direction, range_select)
    wind_direction_full = filter_by_analysis_period(epw.wind_direction, range_full)
    wind_direction_day = filter_by_analysis_period(epw.wind_direction, range_day)
    
    direction_values_select = wind_direction_select.values
    direction_values_full = wind_direction_full.values
    direction_values_day = wind_direction_day.values

    # 处理颜色映射
    min_speed_select = np.min(speed_values_select)
    max_speed_select = np.max(speed_values_select)
    min_speed_full = np.min(speed_values_full)
    max_speed_full = np.max(speed_values_full)

    color_values_select_speed = [map_to_color(speed, min_speed_select, max_speed_select, color_scheme) for speed in speed_values_select]
    color_values_full_speed = [map_to_color(speed, min_speed_full, max_speed_full, color_scheme) for speed in speed_values_full]

    # 计算日均风速
    daily_averages_speed = calculate_daily_averages(speed_values_day, wind_speed_day.datetimes)
    min_speed_daily_avg = daily_averages_speed.min()
    max_speed_daily_avg = daily_averages_speed.max()
    color_values_day_speed = [map_to_color(speed, min_speed_daily_avg, max_speed_daily_avg, color_scheme) for speed in daily_averages_speed]

    # 生成每月的风速均值
    monthly_averages_speed = calculate_monthly_averages(speed_values_full, wind_speed_full.datetimes)
    min_avg_speed = monthly_averages_speed.min()
    max_avg_speed = monthly_averages_speed.max()
    avg_color_values_speed = [map_to_color(speed, min_avg_speed, max_avg_speed, color_scheme) for speed in monthly_averages_speed]
    # 计算一些总结性统计数据
    total_avg_speed = monthly_averages_speed.mean()
    slowest_month = monthly_averages_speed.idxmin()
    fastest_month = monthly_averages_speed.idxmax()
    speed_difference = max_avg_speed - min_avg_speed

    # 计算盛行风向
    wind_rose_month = WindRose(wind_direction_select, wind_speed_select, 32)
    wind_rose_year = WindRose(wind_direction_full, wind_speed_full, 32)
    prevailing_direction_month = wind_rose_month.prevailing_direction
    prevailing_direction_year = wind_rose_year.prevailing_direction

    # 获取风向名称
    prevailing_direction_month_name = str("该城市的月盛行风向" + get_wind_direction_name(prevailing_direction_month))
    prevailing_direction_year_name = str("该城市的年盛行风向" + get_wind_direction_name(prevailing_direction_year))
    monthly_text = str(
    f"从全年来看，总的平均风速是{total_avg_speed:.2f} m/s，"
    f"最高风速出现在{fastest_month}月，为{monthly_averages_speed.max():.2f} m/s，"
    f"最低风速出现在{slowest_month}月，为{monthly_averages_speed.min():.2f} m/s，"
    f"最高风速月与最低风速月之间的风速差值为{speed_difference:.2f} m/s"
    )
        
    daily_text = str(
        f"当前月份的平均风速是{daily_averages_speed.mean():.2f} m/s，"
        f"最高风速是{max_speed_daily_avg:.2f} m/s，最低风速是{min_speed_daily_avg:.2f} m/s"
    )
    if show_charts:
        # 生成每小时的风速柱状图
        fig_speed1 = generate_bar_chart(
            speed_values_select,
            f"Hourly Wind Speed ({start_month} to {end_month} Month)",
            "Hour",
            "Wind Speed (m/s)",
            color_values_select_speed
        )
        # 生成每日的风速柱状图
        fig_speed2 = generate_bar_chart(
            daily_averages_speed,
            f"Daily Wind Speed ({start_month} to {end_month} Month)",
            "Day",
            "Daily Average Wind Speed (m/s)",
            color_values_day_speed
        )
        # 生成风玫瑰图
        legend_parameters = generate_legend_parameters(color_scheme)
        title = "Wind Rose Diagram"
        fig_wind_rose = generate_wind_rose(wind_direction_full, wind_speed_full, range_full, legend_parameters, title)
    
        # 生成每月的风速柱状图
        fig_speed3 = generate_bar_chart(
            monthly_averages_speed,
            "Monthly Average Wind Speed",
            "Month",
            "Average Wind Speed (m/s)",
            avg_color_values_speed
        )
        fig_speed3.update_xaxes(tickvals=list(range(1, 13)), ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

        # 显示图
        chart_selection = st.radio('Select Chart to Display', ['Hourly Wind Speed', 'Daily Wind Speed', 'Monthly Average Wind Speed', 'Wind Rose Diagram'])
        if chart_selection == 'Hourly Wind Speed':
            st.plotly_chart(fig_speed1, use_container_width=True)
        elif chart_selection == 'Daily Wind Speed':
            st.plotly_chart(fig_speed2, use_container_width=True)
        elif chart_selection == 'Monthly Average Wind Speed':
            st.plotly_chart(fig_speed3, use_container_width=True)
        else:
            st.plotly_chart(fig_wind_rose, use_container_width=True)

        # 新增AI分析按钮
        if st.button('Current Month and Annual Wind Speed Analysis'):
            advice = generate_wind_analysis_advice(monthly_text, daily_text, prevailing_direction_month_name, prevailing_direction_year_name)
            st.markdown(f"**AI分析结果:**\n{advice}")

    return f"{monthly_text}\n{daily_text}"
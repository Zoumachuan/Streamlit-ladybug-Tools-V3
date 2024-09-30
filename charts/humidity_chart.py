# humidity_chart.py

import streamlit as st
import numpy as np
from utils.chart_generator import generate_bar_chart
from utils.data_processor import filter_by_analysis_period, calculate_daily_averages, calculate_monthly_averages
from utils.template_base import map_to_color
from utils.openai_integration import generate_humidity_analysis_advice
from ladybug.analysisperiod import AnalysisPeriod

def generate_humidity_charts(epw, start_month, end_month, color_scheme):
    """
    生成湿度相关图表。

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

    # 获取相对湿度数据
    humidity_select = filter_by_analysis_period(epw.relative_humidity, range_select)
    humidity_full = filter_by_analysis_period(epw.relative_humidity, range_full)
    humidity_day = filter_by_analysis_period(epw.relative_humidity, range_day)
    
    humidity_values_select = humidity_select.values
    humidity_values_full = humidity_full.values
    humidity_values_day = humidity_day.values

    # 处理颜色映射
    min_humidity_select = np.min(humidity_values_select)
    max_humidity_select = np.max(humidity_values_select)
    min_humidity_full = np.min(humidity_values_full)
    max_humidity_full = np.max(humidity_values_full)

    color_values_select_humidity = [map_to_color(humidity, min_humidity_select, max_humidity_select, color_scheme) for humidity in humidity_values_select]
    color_values_full_humidity = [map_to_color(humidity, min_humidity_full, max_humidity_full, color_scheme) for humidity in humidity_values_full]
    
    # 生成每小时的相对湿度柱状图
    fig_humidity1 = generate_bar_chart(
        humidity_values_select,
        f"Hourly Relative Humidity ({start_month} to {end_month} Month)",
        "Hour",
        "Relative Humidity (%)",
        color_values_select_humidity
    )
    
    # 计算日均湿度
    daily_averages_humidity = calculate_daily_averages(humidity_values_day, humidity_day.datetimes)
    min_humidity_daily_avg = daily_averages_humidity.min()
    max_humidity_daily_avg = daily_averages_humidity.max()
    color_values_day_humidity = [map_to_color(humidity, min_humidity_daily_avg, max_humidity_daily_avg, color_scheme) for humidity in daily_averages_humidity]

    # 生成每日的相对湿度柱状图
    fig_humidity2 = generate_bar_chart(
        daily_averages_humidity,
        f"Daily Relative Humidity ({start_month} to {end_month} Month)",
        "Day",
        "Daily Average Relative Humidity (%)",
        color_values_day_humidity
    )

    # 计算每月的相对湿度均值
    monthly_averages_humidity = calculate_monthly_averages(humidity_values_full, humidity_full.datetimes)
    min_avg_humidity = monthly_averages_humidity.min()
    max_avg_humidity = monthly_averages_humidity.max()
    avg_color_values_humidity = [map_to_color(humidity, min_avg_humidity, max_avg_humidity, color_scheme) for humidity in monthly_averages_humidity]
    
    # 生成每月的相对湿度柱状图
    fig_humidity3 = generate_bar_chart(
        monthly_averages_humidity,
        "Monthly Average Relative Humidity",
        "Month",
        "Average Relative Humidity (%)",
        avg_color_values_humidity
    )
    fig_humidity3.update_xaxes(tickvals=list(range(1, 13)), ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

    # 显示图表
    chart_selection = st.radio('Select Chart to Display', ['Hourly Relative Humidity', 'Daily Relative Humidity', 'Monthly Average Relative Humidity'])
    if chart_selection == 'Hourly Relative Humidity':
        st.plotly_chart(fig_humidity1, use_container_width=True)
    elif chart_selection == 'Daily Relative Humidity':
        st.plotly_chart(fig_humidity2, use_container_width=True)
    else:
        st.plotly_chart(fig_humidity3, use_container_width=True)
    
    # 计算一些总结性统计数据
    total_avg_humidity = monthly_averages_humidity.mean()
    lowest_humidity_month = monthly_averages_humidity.idxmin()
    highest_humidity_month = monthly_averages_humidity.idxmax()
    humidity_difference = max_avg_humidity - min_avg_humidity
    current_month_avg_humidity = daily_averages_humidity.mean()
    max_humidity_daily_avg = daily_averages_humidity.max()
    min_humidity_daily_avg = daily_averages_humidity.min()
    
    monthly_text = str(
        f"从全年来看，总的平均相对湿度是{total_avg_humidity:.2f}%，"
        f"最高相对湿度出现在{highest_humidity_month}月，为{min_avg_humidity:.2f}%，"
        f"最低相对湿度出现在{lowest_humidity_month}月，为{max_avg_humidity:.2f}%，"
        f"最高湿度月与最低湿度月之间的相对湿度差为{humidity_difference:.2f}%"
    )

    daily_text = str(
        f"当前月份的平均相对湿度是{current_month_avg_humidity:.2f}%，"
        f"最高相对湿度是{max_humidity_daily_avg:.2f}%，最低相对湿度是{min_humidity_daily_avg:.2f}%"
    )

    # 新增AI分析按钮
    if st.button('Evaluate Current Month and Annual Relative Humidity'):
        advice = generate_humidity_analysis_advice(monthly_text, daily_text)
        st.markdown(f"**AI分析结果:**\n{advice}")

# radiation_chart.py

import streamlit as st
import numpy as np
from utils.chart_generator import generate_bar_chart
from utils.data_processor import filter_by_analysis_period, calculate_daily_averages, calculate_monthly_averages
from utils.template_base import map_to_color
from utils.openai_integration import generate_radiation_analysis_advice
from ladybug.analysisperiod import AnalysisPeriod

def generate_radiation_charts(epw, start_month, end_month, color_scheme, rad_type, show_charts=True):
    """
    生成辐射相关图表。

    Args:
        epw (EPW): 加载的EPW对象。
        start_month (int): 起始月份。
        end_month (int): 终止月份。
        color_scheme (int): 色卡编号。
        rad_type (str): 辐射类型（"Direct", "Diffuse", "Global"之一）。
        show_charts (bool): 是否显示图表。
    """
    # 创建分析周期
    range_select = AnalysisPeriod(st_month=start_month, end_month=end_month)
    range_full = AnalysisPeriod(st_month=1, end_month=12)
    range_day = AnalysisPeriod(st_month=start_month, st_day=1, end_month=end_month, end_day=31)

    # 根据辐射类型选择数据
    if rad_type == "Direct":
        rad_select = filter_by_analysis_period(epw.direct_normal_radiation, range_select)
        rad_full = filter_by_analysis_period(epw.direct_normal_radiation, range_full)
        rad_day = filter_by_analysis_period(epw.direct_normal_radiation, range_day)
        y_label = "Direct Normal Radiation (W/m²)"
    elif rad_type == "Diffuse":
        rad_select = filter_by_analysis_period(epw.diffuse_horizontal_radiation, range_select)
        rad_full = filter_by_analysis_period(epw.diffuse_horizontal_radiation, range_full)
        rad_day = filter_by_analysis_period(epw.diffuse_horizontal_radiation, range_day)
        y_label = "Diffuse Horizontal Radiation (W/m²)"
    elif rad_type == "Global":
        rad_select = filter_by_analysis_period(epw.global_horizontal_radiation, range_select)
        rad_full = filter_by_analysis_period(epw.global_horizontal_radiation, range_full)
        rad_day = filter_by_analysis_period(epw.global_horizontal_radiation, range_day)
        y_label = "Global Horizontal Radiation (W/m²)"

    radiation_values_select = rad_select.values
    radiation_values_full = rad_full.values
    radiation_values_day = rad_day.values

    # 处理颜色映射
    min_rad_select = np.min(radiation_values_select)
    max_rad_select = np.max(radiation_values_select)
    min_rad_full = np.min(radiation_values_full)
    max_rad_full = np.max(radiation_values_full)

    color_values_select = [map_to_color(rad, min_rad_select, max_rad_select, color_scheme) for rad in radiation_values_select]
    color_values_full = [map_to_color(rad, min_rad_full, max_rad_full, color_scheme) for rad in radiation_values_full]
    
    # 计算日均辐射
    daily_averages_rad = calculate_daily_averages(radiation_values_day, rad_day.datetimes)
    min_rad_daily_avg = daily_averages_rad.min()
    max_rad_daily_avg = daily_averages_rad.max()
    color_values_day_rad = [map_to_color(rad, min_rad_daily_avg, max_rad_daily_avg, color_scheme) for rad in daily_averages_rad]

    # 计算每月的辐射均值
    monthly_averages_rad = calculate_monthly_averages(radiation_values_full, rad_full.datetimes)
    min_avg_rad = monthly_averages_rad.min()
    max_avg_rad = monthly_averages_rad.max()
    avg_color_values_rad = [map_to_color(rad, min_avg_rad, max_avg_rad, color_scheme) for rad in monthly_averages_rad]

    # 计算一些总结性统计数据
    total_avg_rad = monthly_averages_rad.mean()
    lowest_rad_month = monthly_averages_rad.idxmin()
    highest_rad_month = monthly_averages_rad.idxmax()
    rad_difference = max_avg_rad - min_avg_rad
    current_month_avg_rad = daily_averages_rad.mean()
    max_rad_daily_avg = daily_averages_rad.max()
    min_rad_daily_avg = daily_averages_rad.min()
    
    monthly_text = str(
        f"从全年来看，总的平均{rad_type}辐射是{total_avg_rad:.2f} W/m²，"
        f"最高{rad_type}辐射出现在{highest_rad_month}月，为{max_avg_rad:.2f} W/m²，"
        f"最低{rad_type}辐射出现在{lowest_rad_month}月，为{min_avg_rad:.2f} W/m²，"
        f"最高辐射月与最低辐射月之间的{rad_type}辐射差为{rad_difference:.2f} W/m²"
    )

    daily_text = str(
        f"当前月份的平均{rad_type}辐射是{current_month_avg_rad:.2f} W/m²，"
        f"最高{rad_type}辐射是{max_rad_daily_avg:.2f} W/m²，最低{rad_type}辐射是{min_rad_daily_avg:.2f} W/m²"
    )

    if show_charts:
        # 生成每小时的辐射柱状图
        fig_rad1 = generate_bar_chart(
            radiation_values_select,
            f"Hourly {y_label} ({start_month}-{end_month} Month)",
            "Hour",
            y_label,
            color_values_select
        )

        # 生成每日的辐射柱状图
        fig_rad2 = generate_bar_chart(
            daily_averages_rad,
            f"Daily {y_label} ({start_month}-{end_month} Month)",
            "Day",
            f"Daily Average {y_label}",
            color_values_day_rad
        )

        # 生成每月的辐射柱状图
        fig_rad3 = generate_bar_chart(
            monthly_averages_rad,
            f"Monthly Average {y_label}",
            "Month",
            f"Average {y_label}",
            avg_color_values_rad
        )
        fig_rad3.update_xaxes(tickvals=list(range(1, 13)), ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

        # 显示图表
        chart_selection = st.radio('Select Chart to Display', ['Hourly Radiation', 'Daily Radiation', 'Monthly Average Radiation'])
        if chart_selection == 'Hourly Radiation':
            st.plotly_chart(fig_rad1, use_container_width=True)
        elif chart_selection == 'Daily Radiation':
            st.plotly_chart(fig_rad2, use_container_width=True)
        else:
            st.plotly_chart(fig_rad3, use_container_width=True)
        
        # 新增AI分析按钮
        if st.button(f'Evaluate Current Month and Annual {rad_type} Radiation'):
            advice = generate_radiation_analysis_advice(monthly_text, daily_text, rad_type)
            st.markdown(f"**AI分析结果:**\n{advice}")

    return f"{monthly_text}\n{daily_text}"

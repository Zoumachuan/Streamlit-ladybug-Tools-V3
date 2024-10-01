# illuminance_chart.py

import streamlit as st
import numpy as np
from utils.chart_generator import generate_bar_chart
from utils.data_processor import filter_by_analysis_period, calculate_daily_averages, calculate_monthly_averages
from utils.template_base import map_to_color
from utils.openai_integration import generate_illuminance_analysis_advice
from ladybug.analysisperiod import AnalysisPeriod

def generate_illuminance_charts(epw, start_month, end_month, color_scheme, ill_type, show_charts=True):
    """
    生成照度相关图表。

    Args:
        epw (EPW): 加载的EPW对象。
        start_month (int): 起始月份。
        end_month (int): 终止月份。
        color_scheme (int): 色卡编号。
        ill_type (str): 照度类型（"Direct", "Diffuse", "Global"之一）。
        show_charts (bool): 是否显示图表。
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
    
    # 计算日均照度
    daily_averages_ill = calculate_daily_averages(illuminance_values_day, ill_day.datetimes)
    min_ill_daily_avg = daily_averages_ill.min()
    max_ill_daily_avg = daily_averages_ill.max()
    color_values_day_ill = [map_to_color(ill, min_ill_daily_avg, max_ill_daily_avg, color_scheme) for ill in daily_averages_ill]

    # 计算每月的照度均值
    monthly_averages_ill = calculate_monthly_averages(illuminance_values_full, ill_full.datetimes)
    min_avg_ill = monthly_averages_ill.min()
    max_avg_ill = monthly_averages_ill.max()
    avg_color_values_ill = [map_to_color(ill, min_avg_ill, max_avg_ill, color_scheme) for ill in monthly_averages_ill]

    # 计算一些总结性统计数据
    total_avg_ill = monthly_averages_ill.mean()
    lowest_ill_month = monthly_averages_ill.idxmin()
    highest_ill_month = monthly_averages_ill.idxmax()
    ill_difference = max_avg_ill - min_avg_ill
    current_month_avg_ill = daily_averages_ill.mean()
    max_ill_daily_avg = daily_averages_ill.max()
    min_ill_daily_avg = daily_averages_ill.min()
    
    monthly_text = str(
        f"从全年来看，总的平均{ill_type}照度是{total_avg_ill:.2f}lux，"
        f"最高{ill_type}照度出现在{highest_ill_month}月，为{max_avg_ill:.2f}lux，"
        f"最低{ill_type}照度出现在{lowest_ill_month}月，为{min_avg_ill:.2f}lux，"
        f"最高照度月与最低照度月之间的{ill_type}照度差为{ill_difference:.2f}lux"
    )

    daily_text = str(
        f"当前月份的平均{ill_type}照度是{current_month_avg_ill:.2f}lux，"
        f"最高{ill_type}照度是{max_ill_daily_avg:.2f}lux，最低{ill_type}照度是{min_ill_daily_avg:.2f}lux"
    )

    if show_charts:
        # 生成每小时的照度柱状图
        fig_ill1 = generate_bar_chart(
            illuminance_values_select,
            f"Hourly {y_label} ({start_month} to {end_month} Month)",
            "Hour",
            y_label,
            color_values_select
        )

        # 生成每日的照度柱状图
        fig_ill2 = generate_bar_chart(
            daily_averages_ill,
            f"Daily {y_label} ({start_month} to {end_month} Month)",
            "Day",
            f"Daily Average {y_label}",
            color_values_day_ill
        )

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
        
        # 新增AI分析按钮
        if st.button(f'Evaluate Current Month and Annual {ill_type} Illuminance'):
            advice = generate_illuminance_analysis_advice(monthly_text, daily_text, ill_type)
            st.markdown(f"**AI分析结果:**\n{advice}")

    return f"{monthly_text}\n{daily_text}"

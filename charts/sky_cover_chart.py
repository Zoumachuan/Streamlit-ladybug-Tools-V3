# sky_cover_chart.py

import streamlit as st
import numpy as np
from utils.chart_generator import generate_bar_chart
from utils.data_processor import filter_by_analysis_period, calculate_daily_averages, calculate_monthly_averages
from utils.template_base import map_to_color
from utils.openai_integration import generate_sky_cover_analysis_advice
from ladybug.analysisperiod import AnalysisPeriod

def generate_sky_cover_charts(epw, start_month, end_month, color_scheme,show_charts=True):
    """
    生成天空覆盖量相关图表。

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

    # 获取天空覆盖量数据
    sky_cover_select = filter_by_analysis_period(epw.total_sky_cover, range_select)
    sky_cover_full = filter_by_analysis_period(epw.total_sky_cover, range_full)
    sky_cover_day = filter_by_analysis_period(epw.total_sky_cover, range_day)
    
    sky_cover_values_select = sky_cover_select.values
    sky_cover_values_full = sky_cover_full.values
    sky_cover_values_day = sky_cover_day.values

    # 处理颜色映射
    min_cover_select = np.min(sky_cover_values_select)
    max_cover_select = np.max(sky_cover_values_select)
    min_cover_full = np.min(sky_cover_values_full)
    max_cover_full = np.max(sky_cover_values_full)

    color_values_select = [map_to_color(cover, min_cover_select, max_cover_select, color_scheme) for cover in sky_cover_values_select]
    color_values_full = [map_to_color(cover, min_cover_full, max_cover_full, color_scheme) for cover in sky_cover_values_full]

    # 计算日均天空覆盖量
    daily_averages_cover = calculate_daily_averages(sky_cover_values_day, sky_cover_day.datetimes)
    min_cover_daily_avg = daily_averages_cover.min()
    max_cover_daily_avg = daily_averages_cover.max()
    color_values_day_cover = [map_to_color(cover, min_cover_daily_avg, max_cover_daily_avg, color_scheme) for cover in daily_averages_cover]

    # 计算每月的天空覆盖量均值
    monthly_averages_cover = calculate_monthly_averages(sky_cover_values_full, sky_cover_full.datetimes)
    min_avg_cover = monthly_averages_cover.min()
    max_avg_cover = monthly_averages_cover.max()
    avg_color_values_cover = [map_to_color(cover, min_avg_cover, max_avg_cover, color_scheme) for cover in monthly_averages_cover]

    # 计算一些总结性统计数据
    total_avg_cover = monthly_averages_cover.mean()
    coverless_month = monthly_averages_cover.idxmin()
    coverest_month = monthly_averages_cover.idxmax()
    cover_difference = max_avg_cover - min_avg_cover

    monthly_text = (
        f"从全年来看，总的平均天空覆盖量是{total_avg_cover:.2f}，"
        f"最高天空覆盖量出现在{coverest_month}月，为{max_avg_cover:.2f}，"
        f"最低天空覆盖量出现在{coverless_month}月，为{min_avg_cover:.2f}，"
        f"最高覆盖量月与最低覆盖量月之间的覆盖量差为{cover_difference:.2f}"
    )

    daily_text = (
        f"当前月份的平均天空覆盖量是{(daily_averages_cover.mean()):.2f}，"
        f"最高天空覆盖量是{max_cover_daily_avg:.2f}，最低天空覆盖量是{min_cover_daily_avg:.2f}"
    )


    if show_charts:
        # 生成每小时的天空覆盖量柱状图
        fig_cover1 = generate_bar_chart(
            sky_cover_values_select,
            f"Hourly Total Sky Cover ({start_month} to {end_month} Month)",
            "Hour",
            "Total Sky Cover",
            color_values_select
        )
        


        # 生成每日的天空覆盖量柱状图
        fig_cover2 = generate_bar_chart(
            daily_averages_cover,
            f"Daily Total Sky Cover ({start_month} to {end_month} Month)",
            "Day",
            "Daily Average Total Sky Cover",
            color_values_day_cover
        )


        
        # 生成每月的天空覆盖量柱状图
        fig_cover3 = generate_bar_chart(
            monthly_averages_cover,
            "Monthly Average Total Sky Cover",
            "Month",
            "Average Total Sky Cover",
            avg_color_values_cover
        )
        fig_cover3.update_xaxes(tickvals=list(range(1, 13)), ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

        # 显示图表
        chart_selection = st.radio('Select Chart to Display', ['Hourly Total Sky Cover', 'Daily Total Sky Cover', 'Monthly Average Total Sky Cover'])
        if chart_selection == 'Hourly Total Sky Cover':
            st.plotly_chart(fig_cover1, use_container_width=True)
        elif chart_selection == 'Daily Total Sky Cover':
            st.plotly_chart(fig_cover2, use_container_width=True)
        else:
            st.plotly_chart(fig_cover3, use_container_width=True)
    
        # 新增AI分析按钮
        if st.button('Current Month and Annual Sky Cover Evaluation'):
            advice = generate_sky_cover_analysis_advice(monthly_text, daily_text)
            st.markdown(f"**AI分析结果:**\n{advice}")
            
    return f"{monthly_text}\n{daily_text}"
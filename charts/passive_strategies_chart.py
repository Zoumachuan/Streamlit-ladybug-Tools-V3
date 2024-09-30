# charts/passive_strategies_chart.py

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import math
import pandas as pd
import json
from utils.openai_integration import generate_passive_strategies_advice

def generate_passive_strategies_chart(epw):
    """
    生成被动策略相关图表。

    Args:
        epw (EPW): 加载的EPW对象。
    """
    # 定义状态名称 and 颜色
    states = [
        "Comfort/舒适时段",
        "Sun Shading of windows/窗户遮阳",
        "High Thermal Mass/高热质量",
        "High Thermal Mass Night Flushed/高热质量+夜间通风",
        "Direct Evaporative Cooling/直接蒸发冷却",
        "Two-Stage Evaporative Cooling/双级蒸发冷却",
        "Natural Ventilation Cooling/自然通风冷却",
        "Fan-Forced Ventilation Cooling/风扇通风冷却",
        "Internal Heating Gain/内部加热增益",
        "Humidification Only/仅加湿",
        "Dehumidification Only/仅除湿",
        "Cooling add Dehumidification if needed/制冷除湿",
        "Heating add Humidification if needed/加热增湿",
    ]
    colors = [
        "blue",
        "lightblue",
        "cyan",
        "green",
        "lightgreen",
        "lime",
        "yellow",
        "lightgrey",
        "khaki",
        "orange",
        "darkorange",
        "orange",
        "purple",
    ]
    
    # 初始化状态计数 and 焓比累计
    state_counts = [0] * len(states)
    total_h_sum = 0
    total_h_count = 0
    total_tw_sum = 0
    total_tw_count = 0
    
    # 初始化湿球温度范围计数
    tw_ranges = [0, 0, 0, 0, 0]  # 0-10, 10-20, 20-30, 30-40, 40+
    
    # 初始化焓比范围计数
    h_ranges = [0, 0, 0, 0, 0]  # 0-10, 10-30, 30-50, 50-70, 70+
    
    # 常数 and 计算
    R = 287.05  # 气体常数，单位 J/(kg*K)
    P = 101.325  # 标准大气压，单位 KPa
    
    # 计算每个小时的热湿状态，并分配到不同状态
    for i in range(8760):  # 假设共有8760个小时的数据
        # 获取干球温度、相对湿度、露点温度（假设获取方法如下）
        t_drybulb = epw.dry_bulb_temperature[i]
        rh_percentage = epw.relative_humidity[i] / 100.0
        t_dewpoint = epw.dew_point_temperature[i]
    
        # 计算饱 and 水蒸气压
        e = 6.1078 * math.pow(10, (7.5 * t_drybulb / (t_drybulb + 237.3) - 1))
    
        # 计算含湿量
        d = 0.622 * (rh_percentage * e) / (P - rh_percentage * e)
    
        # 计算湿球温度
        tw = (
            t_drybulb * math.atan(0.152 * math.sqrt(rh_percentage * 100 + 8.3136))
            + math.atan(t_drybulb + rh_percentage)
            - math.atan(rh_percentage * 100 - 1.6763)
            + 0.00391838 * math.pow(rh_percentage * 100, 1.5) * math.atan(0.0231 * rh_percentage * 100)
            - 4.686
        )
    
        # 计算焓比
        h = 1.006 * t_drybulb + (2501 + 1.86 * t_drybulb) * d
    
        # 累计焓比 and 湿球温度
        total_h_sum += h
        total_h_count += 1
        total_tw_sum += tw
        total_tw_count += 1
    
        # 根据湿球温度范围计数
        if 0 <= tw < 10:
            tw_ranges[0] += 1
        elif 10 <= tw < 20:
            tw_ranges[1] += 1
        elif 20 <= tw < 30:
            tw_ranges[2] += 1
        elif 30 <= tw < 40:
            tw_ranges[3] += 1
        elif tw >= 40:
            tw_ranges[4] += 1
    
        # 根据焓比范围计数
        if h < 10:
            h_ranges[0] += 1
        elif 10 <= h < 30:
            h_ranges[1] += 1
        elif 30 <= h < 50:
            h_ranges[2] += 1
        elif 50 <= h < 70:
            h_ranges[3] += 1
        elif h >= 70:
            h_ranges[4] += 1
    
        # 根据条件将小时分配到不同状态
        if rh_percentage < 0.8 and tw < 17 and 20 < t_drybulb < 24:
            state_counts[0] += 1  # Comfort
    
        if rh_percentage > 0.8 and tw > 17 and 20 < t_drybulb:
            state_counts[1] += 1  # Sun Shading of windows
    
        if -4 < t_dewpoint < 18 and tw < 21.5 and rh_percentage < 0.8 and 20 < t_drybulb < 32.5:
            state_counts[2] += 1  # High Thermal Mass
    
        if -4 < t_dewpoint < 18 and t_drybulb > 20 and rh_percentage < 0.8 and tw < 23:
            state_counts[3] += 1  # High Thermal Mass Night Flushed
    
        if 9 < tw < 18 and t_drybulb > 20 and rh_percentage < 0.8:
            state_counts[4] += 1  # Direct Evaporative Cooling
    
        if 9 < tw < 22 and t_drybulb > 20 and rh_percentage < 0.8 and t_dewpoint < 12:
            state_counts[5] += 1  # Two-Stage Evaporative Cooling
    
        if 20 < t_drybulb < 26.5 and -5 < t_dewpoint and  0.15 < rh_percentage < 0.9 and tw < 23:
            state_counts[6] += 1  # Natural Ventilation Cooling
    
        if 20 < t_drybulb < 28 and -5 < t_dewpoint and 0.15 < rh_percentage < 0.9 and tw < 23:
            state_counts[7] += 1  # Fan-Forced Ventilation Cooling
    
        if 12.5 < t_drybulb < 20:
            state_counts[8] += 1  # Internal Heating Gain
    
        if t_dewpoint < -4 and 20 < t_drybulb < 24:
            state_counts[9] += 1  # Humidification Only
    
        if rh_percentage > 0.8 and tw > 17 and 20 < t_drybulb < 24:
            state_counts[10] += 1  # Dehumidification Only
    
        if t_drybulb > 24:
            state_counts[11] += 1  # Cooling add Dehumidification if needed
    
        if t_drybulb < 20:
            state_counts[12] += 1  # Heating add Humidification if needed
    
    # 计算分布比例
    total_hours = 8760  # 假设共有8760个小时的数据
    state_distribution = [count for count in state_counts]
    
    # 创建彩色条
    fig = go.Figure(data=[go.Bar(x=state_distribution, y=states, orientation="h", marker_color=colors)])
    
    # 设置图表布局
    fig.update_layout(
        title="Passive Strategies/被动策略",
        xaxis_title="Hour Count/占比小时数",
        yaxis_title="States/策略",
        yaxis_categoryorder="total ascending",
    )
    
    # 绘制图表
    st.plotly_chart(fig, use_container_width=True)
    
    # 计算被动策略的占比
    passive_strategies_percentages = []
    for i in range(len(states)):
        percentage = (state_distribution[i] / total_hours) * 100
        passive_strategies_percentages.append(percentage)

    # 将图表整理成文字形式
    chart_text = ""
    for i in range(len(states)):
        chart_text += f"{states[i]} 占比 {passive_strategies_percentages[i]:.2f}%\n"

    # 新增AI分析按钮
    if st.button('Obtain passive strategy recommendations'):
        advice = generate_passive_strategies_advice(chart_text)
        st.markdown(f"**AI分析结果:**\n{advice}")

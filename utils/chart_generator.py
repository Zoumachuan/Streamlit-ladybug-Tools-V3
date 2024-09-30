# chart_generator.py

import plotly.graph_objects as go
from utils.data_processor import filter_by_analysis_period, calculate_monthly_averages, calculate_daily_averages

def generate_bar_chart(data, title, x_label, y_label, color_values):
    """
    生成柱状图。

    Args:
        data (list): 要可视化的数据值列表。
        title (str): 图表标题。
        x_label (str): x轴标签。
        y_label (str): y轴标签。
        color_values (list): 每个柱的颜色列表。

    Returns:
        plotly.graph_objects.Figure: 生成的柱状图。
    """
    fig = go.Figure(data=[go.Bar(x=list(range(len(data))), y=data, marker_color=color_values)])
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label
    )
    return fig

def generate_wind_rose(wind_directions, wind_speeds, analysis_period, legend_parameters, title):
    """
    生成风玫瑰图并添加标题。

    Args:
        wind_directions (TimeSeries): 风向数据。
        wind_speeds (TimeSeries): 风速数据。
        analysis_period (AnalysisPeriod): 分析周期。
        legend_parameters (LegendParameters): 图例参数。
        title (str): 图表标题。

    Returns:
        plotly.graph_objects.Figure: 生成的风玫瑰图。
    """
    from ladybug.windrose import WindRose
    from ladybug_charts import to_figure

    wind_directions_filtered = filter_by_analysis_period(wind_directions, analysis_period)
    wind_speeds_filtered = filter_by_analysis_period(wind_speeds, analysis_period)

    wind_rose = WindRose(wind_directions_filtered, wind_speeds_filtered)
    wind_rose.legend_parameters = legend_parameters

    figure = to_figure.wind_rose(wind_rose)

    # 添加标题
    figure.update_layout(title=title)

    return figure
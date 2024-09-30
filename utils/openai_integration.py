# openai_integration.py

import http.client
import json
from config import get_api_credentials
import streamlit as st

def get_openai_response(prompt):
    openai_api_scheme, openai_api_host, openai_api_key = get_api_credentials()

    geoinfo = st.session_state.get('geoinfo', '未知区域')  # 获取 geoinfo 或者使用默认值

    conn = http.client.HTTPConnection(openai_api_host)
    if openai_api_scheme == "https":
        conn = http.client.HTTPSConnection(openai_api_host)

    system_content = "用中文回答问题。"
    if geoinfo:
        system_content += f" 地理编码: {geoinfo}，这个地理编码包含了大洲、城市、国家以及下属行政规划和具体城市的信息，举个例子，WMO_Region_2_Asia/CHN_China/SN_Shaanxi/CHN_SN_Xian.570360_CSWD代表着亚洲中国陕西省西安市，在对该地区进行分析时要结合地理编码所包含的地理信息进行分析"

    payload = json.dumps({
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    })
    headers = {
        'Authorization': f'Bearer {openai_api_key}',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/v1/chat/completions", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))

    if "choices" not in data:
        return "服务器繁忙或出现错误，请重试/The server is busy or experiencing errors, please try again"

    content = data["choices"][0]["message"]["content"]
    return content

def generate_passive_strategies_advice(chart_text):
    """
    生成被动式策略建议。

    Args:
        chart_text (str): 图表文本信息。

    Returns:
        str: 被动式策略建议。
    """
    prompt = (f"在你进行内容输出时，应当让语言尽可能自然，不要机械式的介绍和分析，你现在是一个研究建筑被动式策略的专家，当前城市焓湿图计算结果如下：{chart_text}，请先根据你已知的信息，分享这座城市的信息，包括大洲、国家、行政区划和城市名（中文或翻译成中文），你在输出时请使用自然语言，不要出现地理编码信息，并从地理学的角度介绍这座城市的信息"
              "你需要针对这些数据提供对于该地区建筑采取被动式策略的具体建议,同时将这些策略中占比时长前六的策略借由占比时长从长到短依次排列，"
              "且对其进行有关具体措施的介绍。"
              "你的输出格式应该为：{city_name}市位于{continent_name}州{country_name}国{region_name}省/其他行政区，其气候特点和地理特点为{information}，以下为分析结果：{result}"
              )
              
    return get_openai_response(prompt)

def generate_temperature_analysis_advice(monthly_text, daily_text):
    """
    生成气温数据分析建议。

    Args:
        monthly_text (str): 月数据文本信息。
        daily_text (str): 日数据文本信息。

    Returns:
        str: 气温数据分析建议。
    """
    prompt = (f"在你进行内容输出时，应当让语言尽可能自然，不要机械式的介绍和分析，你现在是一个从事绿色建筑相关专业的气候数据分析师，当前月份的气温数据和该城市全年的气温数据如下：{daily_text}，{monthly_text}，请先根据你已知的信息，分享这座城市的信息，包括大洲、国家、行政区划和城市名（中文或翻译成中文），你在输出时请使用自然语言，不要出现地理编码信息，并从地理学的角度介绍这座城市的信息"
              "请你以以上数据为基础详略得当的介绍当前月份的气温与该城市全年的气温，将当前月份气温与全年气温相对比，并指出这些数据如何影响当地建筑设计，"
              "注意，如果属于某种温度的月份有0个月，则将其忽略。"
              "你的输出格式应该为：{city_name}市位于{continent_name}州{country_name}国{region_name}省/其他行政区，其气候特点和地理特点为{information}，以下为分析结果：{result}"
              )
              
    return get_openai_response(prompt)

def generate_humidity_analysis_advice(monthly_text, daily_text):
    """
    生成相对湿度数据分析建议。

    Args:
        monthly_text (str): 月数据文本信息。
        daily_text (str): 日数据文本信息。

    Returns:
        str: 相对湿度数据分析建议。
    """
    prompt = (f"在你进行内容输出时，应当让语言尽可能自然，不要机械式的介绍和分析，你现在是一个从事绿色建筑相关专业的气候数据分析师，当前月份的相对湿度数据和该城市全年的相对湿度数据如下：{daily_text}，{monthly_text}，请先根据你已知的信息，分享这座城市的信息，包括大洲、国家、行政区划和城市名（中文或翻译成中文），你在输出时请使用自然语言，不要出现地理编码信息，并从地理学的角度介绍这座城市的信息"
              "请你以以上数据为基础详略得当的介绍当前月份的相对湿度与该城市全年的相对湿度，将当前月份相对湿度与全年相对比，"
              "并指出这些数据如何影响当地建筑设计。"
              "你的输出格式应该为：{city_name}市位于{continent_name}州{country_name}国{region_name}省/其他行政区，其气候特点和地理特点为{information}，以下为分析结果：{result}"
              )
              
    return get_openai_response(prompt)

def generate_wind_analysis_advice(monthly_text, daily_text, prevailing_direction_month, prevailing_direction_year):
    """
    生成风速和风向数据分析建议。

    Args:
        monthly_text (str): 月数据文本信息。
        daily_text (str): 日数据文本信息。
        prevailing_direction_month (str): 当前月份的盛行风向。
        prevailing_direction_year (str): 全年的盛行风向。

    Returns:
        str: 风速和风向数据分析建议。
    """
    prompt = (f"在你进行内容输出时，应当让语言尽可能自然，不要机械式的介绍和分析，你现在是一个从事绿色建筑相关专业的气候数据分析师，当前月份的风速和该城市全年的风速数据如下：{daily_text}，{monthly_text}，请先根据你已知的信息，分享这座城市的信息，包括大洲、国家、行政区划和城市名（中文或翻译成中文），你在输出时请使用自然语言，不要出现地理编码信息，并从地理学的角度介绍这座城市的信息"
              f"同时当前月份的盛行风向为{prevailing_direction_month}，全年的盛行风向为{prevailing_direction_year}，"
              "请你以以上数据为基础详略得当的介绍当前月份的风速风向与该城市全年的风速风向，将当前月份风速风向与全年风速风向对比，"
              "并指出这些数据如何影响当地建筑设计。"
              "你的输出格式应该为：{city_name}市位于{continent_name}州{country_name}国{region_name}省/其他行政区，其气候特点和地理特点为{information}，以下为分析结果：{result}"
              )
              
    return get_openai_response(prompt)

def generate_sky_cover_analysis_advice(monthly_text, daily_text):
    """
    生成天空覆盖量数据分析建议。

    Args:
        monthly_text (str): 月数据文本信息。
        daily_text (str): 日数据文本信息。

    Returns:
        str: 天空覆盖量数据分析建议。
    """
    prompt = (f"在你进行内容输出时，应当让语言尽可能自然，不要机械式的介绍和分析，你现在是一个从事绿色建筑相关专业的气候数据分析师，当前月份的天空覆盖量数据和该城市全年的天空覆盖量数据如下：{daily_text}，{monthly_text}，请先根据你已知的信息，分享这座城市的信息，包括大洲、国家、行政区划和城市名（中文或翻译成中文），你在输出时请使用自然语言，不要出现地理编码信息，并从地理学的角度介绍这座城市的信息"
              "请你以以上数据为基础详略得当的介绍当前月份的天空覆盖量与该城市全年的天空覆盖量，将当前月份天空覆盖量与全年天空覆盖量相对比，"
              "并指出这些数据如何影响当地建筑设计。"
              "你的输出格式应该为：{city_name}市位于{continent_name}州{country_name}国{region_name}省/其他行政区，其气候特点和地理特点为{information}，以下为分析结果：{result}"
              )
              
    return get_openai_response(prompt)

def generate_radiation_analysis_advice(monthly_text, daily_text, type):
    """
    生成辐射数据分析建议。

    Args:
        monthly_text (str): 月数据文本信息。
        daily_text (str): 日数据文本信息。
        type (str): 辐射类型（"Direct" 或 "Diffuse" 或 "Global"）。

    Returns:
        str: 辐射数据分析建议。
    """
    prompt = (f"在你进行内容输出时，应当让语言尽可能自然，不要机械式的介绍和分析，你现在是一个从事绿色建筑相关专业的气候数据分析师，当前月份的{type}辐射数据和该城市全年的{type}辐射数据如下：{daily_text}，{monthly_text}，请先根据你已知的信息，分享这座城市的信息，包括大洲、国家、行政区划和城市名（中文或翻译成中文），你在输出时请使用自然语言，不要出现地理编码信息，并从地理学的角度介绍这座城市的信息"
              f"请你以以上数据为基础详略得当的介绍当前月份的{type}辐射与该城市全年的{type}辐射，将当前月份{type}辐射与全年{type}辐射相对比，"
              "并指出这些数据如何影响当地建筑设计。"
              "你的输出格式应该为：{city_name}市位于{continent_name}州{country_name}国{region_name}省/其他行政区，其气候特点和地理特点为{information}，以下为分析结果：{result}"
              )
              
    return get_openai_response(prompt)

def generate_illuminance_analysis_advice(monthly_text, daily_text, type):
    """
    生成照度数据分析建议。

    Args:
        monthly_text (str): 月数据文本信息。
        daily_text (str): 日数据文本信息。
        type (str): 照度类型（"Direct" 或 "Diffuse" 或 "Global"）。

    Returns:
        str: 照度数据分析建议。
    """
    prompt = (f"在你进行内容输出时，应当让语言尽可能自然，不要机械式的介绍和分析，你现在是一个从事绿色建筑相关专业的气候数据分析师，当前月份的{type}照度数据和该城市全年的{type}照度数据如下：{daily_text}，{monthly_text}，请先根据你已知的信息，分享这座城市的信息，包括大洲、国家、行政区划和城市名（中文或翻译成中文），你在输出时请使用自然语言，不要出现地理编码信息，并从地理学的角度介绍这座城市的信息"
              f"请你以以上数据为基础详略得当的介绍当前月份的{type}照度与该城市全年的{type}照度，将当前月份{type}照度与全年{type}照度相对比，"
              "并指出这些数据如何影响当地建筑设计。"
              "你的输出格式应该为：{city_name}市位于{continent_name}州{country_name}国{region_name}省/其他行政区，其气候特点和地理特点为{information}，以下为分析结果：{result}"
              )
              
    return get_openai_response(prompt)

# main.py (Updated)

import streamlit as st
import http.client
import json
import requests
import os
import tempfile
from utils.template_base import set_user_defined_colors
from utils.data_loader import unzip_and_load_epw, load_uploaded_epw
from charts.temperature_chart import generate_temperature_charts
from charts.humidity_chart import generate_humidity_charts
from charts.wind_chart import generate_wind_charts
from charts.sky_cover_chart import generate_sky_cover_charts
from charts.radiation_chart import generate_radiation_charts
from charts.illuminance_chart import generate_illuminance_charts
from charts.passive_strategies_chart import generate_passive_strategies_chart
from charts.artificial_intelligence_zone import generate_ai_report

ALIST_URL = "warehouse.archknowledge.com.cn"
ALIST_AUTHORIZATION = "alist-79f0737a-97a0-4c5f-a51e-df4afecd5d44dB1P9QSM5FRCJbUc0HrywajGijam55RFS1hSvLCGLviwwGhsoqtcaGGcByeg7ELM"

def fetch_file_list(path="/"):
    conn = http.client.HTTPConnection(ALIST_URL)
    payload = json.dumps({"path": path, "password": "", "page": 1, "per_page": 0, "refresh": False})
    headers = {
        'Authorization': ALIST_AUTHORIZATION,
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/api/fs/list", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    
    if data['code'] == 200:
        return data['data']['content']
    else:
        st.error("无法获取文件列表: " + data['message'])
        return []

def download_file(url):
    local_filename = os.path.join(tempfile.gettempdir(), os.path.basename(url))  # 存储在临时目录
    with requests.get(url, stream=True) as r:
        r.raise_for_status()  # 确保请求成功
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def run_app():
    st.header("气象数据与被动策略在线可视化/Visualization of Meteorological Data and Passive Strategies")
    
    continent_folders = fetch_file_list()
    continent_folders = [f for f in continent_folders if f['is_dir']]
    
    epw = None # 初始化 epw 变量

    if continent_folders:
        selected_continent = st.selectbox("选择大洲/Select a continent", [f['name'] for f in continent_folders])

        country_folders = fetch_file_list(f"/{selected_continent}")
        country_folders = [f for f in country_folders if f['is_dir']]

        if country_folders:
            selected_country = st.selectbox("选择国家或地区/Select a country or region", [f['name'] for f in country_folders])
            
            administrative_region_folders = fetch_file_list(f"/{selected_continent}/{selected_country}")
            administrative_region_folders = [f for f in administrative_region_folders if f['is_dir']]
            if administrative_region_folders:
                selected_administrative_region = st.selectbox("选择行政区/Select an administrative region", [f['name'] for f in administrative_region_folders])
                selected_files_path = f"/{selected_continent}/{selected_country}/{selected_administrative_region}"
                selected_files = fetch_file_list(selected_files_path)
            else:
                selected_files_path = f"/{selected_continent}/{selected_country}"
                selected_files = fetch_file_list(selected_files_path)

            selected_files = [f for f in selected_files if not f['is_dir']]
            selected_file = st.selectbox("选择文件/Select a file", [f['name'] for f in selected_files])

            if selected_file and selected_file.endswith(".zip"):
                file_url = f"http://{ALIST_URL}/d{selected_files_path}/{selected_file}"
                geoinfo = file_url.replace("http://warehouse.archknowledge.com.cn/d/", "").replace(".zip", "")
                # 保存 geoinfo 到 session_state
                st.session_state['geoinfo'] = geoinfo

                # 下载文件到临时目录，并获取本地路径
                local_zip_path = download_file(file_url)

                # 使用选中的 ZIP 文件名调用 unzip_and_load_epw，加载 EPW 对象
                epw = unzip_and_load_epw(local_zip_path, selected_file)  
                st.success("成功读取EPW文件/EPW file read successfully!")
                
                # 添加下载按钮
                st.download_button(
                    label="下载已读取的ZIP文件/Download the read ZIP file",
                    data=open(local_zip_path, 'rb'),
                    file_name=selected_file,
                    mime='application/zip'
                )

            uploaded_file = st.file_uploader("上传EPW文件/Upload an EPW file", type="epw")
            if uploaded_file is not None:
                epw = load_uploaded_epw(uploaded_file)
                st.success("成功读取上传的EPW文件/EPW file uploaded successfully!")

            # 检查 epw 是否为 None
            if epw:
                st.subheader('您当前读取的数据是：' + str(epw))
            else:
                st.warning("未读取到有效的数据/No valid data read.")

            # 获取月份
            slider1 = st.slider("起始月份/Start month", 1, 12, key=1)
            slider2 = st.slider("终止月份/End month", 1, 12, key=2)
            start_month = min(slider1, slider2)
            end_month = max(slider1, slider2)

            color_scheme = st.slider("色卡选择，9为自定义颜色/Color Scheme, 9 is custom color", 1, 9, key=3)
            if color_scheme == 9:
                custom_color_1 = st.color_picker("选择第一个颜色/Select the first color", "#FFFFFF")
                custom_color_2 = st.color_picker("选择第二个颜色/Select the second color", "#000000")
                set_user_defined_colors(custom_color_1, custom_color_2)

            data_type = st.selectbox("选择可视化内容/Select Data Type", [
                "人工智能专区/Artificial Intelligence Zone",
                "被动策略/Passive Strategies",
                "温度/Temperature",
                "相对湿度/Relative Humidity",
                "风速和风玫瑰/Wind Speed and Wind Rose",
                "天空覆盖量/Total Sky Cover",
                "直接法线辐射/Direct Normal Rad",
                "散射水平辐射/Diffuse Horizontal Rad",
                "全球水平辐射/Global Horizontal Rad",
                "直接法线照度/Direct Normal Ill",
                "散射水平照度/Diffuse Horizontal Ill",
                "全球水平照度/Global Horizontal Ill"
            ])

            if data_type == "人工智能专区/Artificial Intelligence Zone":
                # 生成图表模块并收集总结信息（不显示图表）
                passive_strategies_summary = generate_passive_strategies_chart(epw, show_charts=False)
                temperature_summary = generate_temperature_charts(epw, start_month, end_month, color_scheme, show_charts=False)
                humidity_summary = generate_humidity_charts(epw, start_month, end_month, color_scheme, show_charts=False)
                wind_summary = generate_wind_charts(epw, start_month, end_month, color_scheme, show_charts=False)
                sky_cover_summary = generate_sky_cover_charts(epw, start_month, end_month, color_scheme, show_charts=False)
                radiation_summary = generate_radiation_charts(epw, start_month, end_month, color_scheme, "Global",show_charts=False)
                illuminance_summary = generate_illuminance_charts(epw, start_month, end_month, color_scheme, "Global",show_charts=False)
                generate_ai_report(
                    passive_strategies_summary=passive_strategies_summary, 
                    temperature_summary=temperature_summary, 
                    humidity_summary=humidity_summary, 
                    wind_summary=wind_summary, 
                    sky_cover_summary=sky_cover_summary,
                    radiation_summary = radiation_summary,
                    illuminance_summary = illuminance_summary
                )
            elif data_type == "被动策略/Passive Strategies":
                generate_passive_strategies_chart(epw)
            elif data_type == "温度/Temperature":
                generate_temperature_charts(epw, start_month, end_month, color_scheme)
            elif data_type == "相对湿度/Relative Humidity":
                generate_humidity_charts(epw, start_month, end_month, color_scheme)
            elif data_type == "风速和风玫瑰/Wind Speed and Wind Rose":
                generate_wind_charts(epw, start_month, end_month, color_scheme)
            elif data_type == "天空覆盖量/Total Sky Cover":
                generate_sky_cover_charts(epw, start_month, end_month, color_scheme)
            elif data_type == "直接法线辐射/Direct Normal Rad":
                generate_radiation_charts(epw, start_month, end_month, color_scheme, "Direct")
            elif data_type == "散射水平辐射/Diffuse Horizontal Rad":
                generate_radiation_charts(epw, start_month, end_month, color_scheme, "Diffuse")
            elif data_type == "全球水平辐射/Global Horizontal Rad":
                generate_radiation_charts(epw, start_month, end_month, color_scheme, "Global")
            elif data_type == "直接法线照度/Direct Normal Ill":
                generate_illuminance_charts(epw, start_month, end_month, color_scheme, "Direct")
            elif data_type == "散射水平照度/Diffuse Horizontal Ill":
                generate_illuminance_charts(epw, start_month, end_month, color_scheme, "Diffuse")
            elif data_type == "全球水平照度/Global Horizontal Ill":
                generate_illuminance_charts(epw, start_month, end_month, color_scheme, "Global")

            # 设置尾部信息
            end_info = ("<font size='2'>Created by <a href='https://zhenzixu.com.cn'>Zhen Zixu</a>,"
                        "Supported by <a href='https://github.com/ymg2007'>Yin Minggang</a>,"
                        "<a href='https://space.bilibili.com/182927334'>Tao Zhengrong</a>,"
                        "<a href='mailto:1121333098@qq.com'>Zhang Xinchi</a>,"
                        "If you have any question or advice, write to <a href='mailto:prof_zhen@126.com'>me</a>.</font>")
            st.write("\n\n\n\n\n" + end_info, unsafe_allow_html=True)
        else:
            st.error("未找到国家或地区文件夹/No country or region folders found.")
    else:
        st.error("未找到包含 'Region' 的大洲文件夹/No continent folders containing 'Region' found.")

if __name__ == "__main__":
    run_app()

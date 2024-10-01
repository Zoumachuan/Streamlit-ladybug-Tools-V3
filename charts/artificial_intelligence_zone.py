# charts/artificial_intelligence_zone.py

from utils.openai_integration import generate_summary
import streamlit as st

# 汇总各个模块的总结文字
def collect_summary_texts(passive_text, temperature_texts, wind_texts, humidity_texts, sky_cover_texts):
    summaries = {
        "passive_strategies": passive_text,
        "temperature": temperature_texts,
        "wind": wind_texts,
        "humidity": humidity_texts,
        "sky_cover": sky_cover_texts
    }
    return summaries

# 生成全面绿建报告
def generate_ai_report(passive_strategies_summary, temperature_summary, humidity_summary, wind_summary, sky_cover_summary, radiation_summary, illuminance_summary):
    """
    生成人工智能绿建报告

    Args:
        passive_strategies_summary (str): 被动策略总结
        temperature_summary (str): 温度总结
        humidity_summary (str): 相对湿度总结
        wind_summary (str): 风速和风玫瑰总结
        sky_cover_summary (str): 天空覆盖总结
    """
    st.subheader("一键生成报告/One click report generation")

    if st.button("生成绿建气候报告/Generate Report"):
        # 汇总所有总结文字
        full_summary = (
            f"被动策略总结:\n{passive_strategies_summary}\n\n"
            f"温度总结:\n{temperature_summary}\n\n"
            f"相对湿度总结:\n{humidity_summary}\n\n"
            f"风速和风玫瑰总结:\n{wind_summary}\n\n"
            f"天空覆盖量总结:\n{sky_cover_summary}\n"
            f"日照辐射总结:\n{radiation_summary}\n"
            f"照度总结:\n{illuminance_summary}\n"
        )

        # 调用 OpenAI 接口生成报告
        report = generate_summary(full_summary)
        st.markdown(report)


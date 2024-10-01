# 🌍 Streamlit-ladybug-Tools-V3.0 🐞

## 项目简介 📖

作为西建大建筑学专业的毕业生，我在学习建筑物理和建筑与城市气候课程时，逐渐接触到了一些能够有效服务于绿色建筑设计的软件和工具。然而，许多设计师和建筑学生在面对形式设计和建筑性能策略时，常常遇到零散且难以解析的问题。这些问题虽然关系到项目的长效节能和环境融合度，却往往被忽视。

为了解决这些痛点，我意识到需要一个既专业又便捷的工具，能够将气候数据和绿色建筑技术结合起来。经过对现有绿色建筑设计软件和工具的研究，我决定开发一个全新的工具。这个工具应当具备以下特点：

- 🌐 **全球化**：用户可以随时获取全球任何地区的气候数据。
- 📊 **直观性**：以图表形式生动展现专业数据。
- 🤖 **智能化**：自动生成被动式设计策略和气候指标评价。
- 🔄 **开放性**：接受用户建议，持续改进。

## 主要功能 ✨

- 🌐 **全球气象数据查询与分析**：涵盖被动式策略、气温、风速风向、湿度、天空覆盖率、照度和辐射等多项数据。
- 🤖 **人工智能总结与建议**：基于分析结果提供绿建建议。
- 📊 **灵活的图表调整**：用户可自由选择月份和图表样式。

## 主要特色 💡

- 🌏 **全球数据在线调用**：随时获取任何地区的气候数据。
- 🧠 **智能分析与建议**：基于绿建知识库提供合理建议。
- 🖼️ **用户友好界面**：直观的图表展示，易于操作。

## 版本更新 🔄

与2.0版本相比，3.0版本进行了全面的重构和优化：

- 🔧 **代码重构**：删除冗余代码，提升代码可读性。
- 🚀 **性能提升**：迁移至高性能服务器。
- 🎨 **自定义色卡**：新增自定义色卡功能。
- 🧩 **人工智能模型优化**：结合实际地理信息进行更合理的分析。

## 安装步骤 🛠️

### 直接使用

[![点击体验](https://img.shields.io/badge/体验一下-007ACC?style=for-the-badge&logo=appveyor&logoColor=white)](http://climate.gbuilding.online/)

### 本地部署

1. 克隆仓库：
   ```bash
   git clone https://github.com/Zoumachuan/Streamlit-ladybug-Tools-V3.0
   ```
2. 修改配置：
   修改 `config.py` 中的 `OPENAI_API_HOST` 和 `OPENAI_API_KEY`。
3. 创建虚拟环境并安装依赖：
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. 运行项目：
   ```bash
   streamlit run main.py
   ```

### 使用 Docker 🐳

1. 克隆仓库：
   ```bash
   git clone https://github.com/Zoumachuan/Streamlit-ladybug-Tools-V3.0
   ```
2. 修改配置：
   修改 `docker-compose.yaml` 中的 `OPENAI_API_HOST` 和 `OPENAI_API_KEY`。
3. 启动 Docker 容器：
   ```bash
   docker-compose up -d
   ```

## 贡献指南 🤝

欢迎各位开发者提交PR！我对Python的使用尚不熟练，期待与绿建行业的同仁和爱好者们共同完善并扩展这个项目。

## 联系方式 📧

如有问题或建议，请联系：prof_zhen@126.com，也欢迎访问来我的个人网站转转！

## 项目结构 🗂️

- `charts/` 存放各种图表生成函数
  - `humidity_chart.py` 用于生成湿度图 💧
  - `illuminance_chart.py` 用于生成照度图 💡
  - `passive_strategies_chart.py` 用于生成被动式策略图 🌱
  - `radiation_chart.py` 用于生成辐射图 ☀️
  - `sky_cover_chart.py` 用于生成天空覆盖率图 ☁️
  - `temperature_chart.py` 用于生成温度图 🌡️
  - `wind_chart.py` 用于生成风玫瑰图 🌬️
- `utils/` 存放各种数据处理函数
  - `chart_generator.py` 用于图表生成 📈
  - `data_loader.py` 用于读取EPW文件 📂
  - `data_processor.py` 用于数据处理 🔄
  - `file_manager.py` 用于文件管理 🗃️
  - `openai_integration.py` 用于人工智能分析 🤖
  - `template_base.py` 用于色卡管理 🎨
- `config.py` 配置文件 ⚙️
- `dockerfile` Docker 配置文件 🐋
- `main.py` 主程序入口 🚪
- `requirements.txt` 依赖库列表 📜

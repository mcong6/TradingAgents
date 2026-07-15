# 02. 财报电话会议深度分析 (Earnings Call Transcripts)

## 1. 目标与价值 (Goal & Value)
美股与 A 股不同，美股公司在每次发布财报时都会举办 **Earnings Call (财报电话会议)**。管理层在 Q&A 环节给出的 **前瞻性指引 (Forward Guidance)** 是华尔街定价的绝对核心。
原版系统的 `Fundamentals Analyst` 只看历史财报数字（利润、营收），这往往是滞后的“后视镜”；接入电话会议记录后，系统将具备前瞻性的基本面判断能力。

## 2. 改造方案 (Implementation Plan)
- **数据源推荐**：
  - **Financial Modeling Prep (FMP)**：直接提供财报电话会议的完整逐字稿 (Transcript API) 和关键点摘要。
  - **AlphaVantage**：同样提供 Earnings 相关的文字总结。
- **核心模块集成点**：
  - 修改 `tradingagents/agents/utils/fundamental_data_tools.py`。
  - 新增工具：`get_latest_earnings_transcript(ticker)`。
  - 如果全文过长（可能超 10k Token），我们需要在工具层做一步**文本截断**，或直接提取管理层的 **Q&A 环节** 和 **Guidance 环节** 供大模型阅读。

## 3. 预期研报输出效果对比 (Expected Output)
- **原版输出**：“上季度营收增长 15%，净利润率提升，基本面稳健。”
- **升级后输出**：“尽管上季度营收增长 15%，但在刚结束的电话会议的 Q&A 环节中，CEO 明确警告下季度供应链成本将飙升，指引不及预期。因此下调评级。”

## 4. 待确认问题 (Open Questions for You)
- 您希望 Agent 阅读**完整的逐字稿全文**（分析更深，但极度消耗 Token），还是阅读**通过工具提前提炼好的摘要**？
- 您是否有可用的 Transcript 数据源？如果没有，我们可以优先考虑接入免费/低成本 API 测试。

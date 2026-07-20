# 数据清洗与降噪层 (Data Scrubbing & Summarization Layer)

本计划旨在借鉴 A 股定制版 Fork 的经验，针对长文本数据（新闻、财报、社交媒体情绪）在传入主脑前增加一层“预处理过滤”，即 **Data Scrubbing Layer**。

## 1. Goal & Value (目标与价值)

在美股分析中，我们经常需要处理长篇大论的数据，例如：
*   **SEC 10-K/10-Q 财报**：动辄几百页，充满法律免责声明和样板文字。
*   **Earnings Call Transcripts (财报电话会记录)**：上万字的对话记录。
*   **Reddit / Twitter / 财经新闻**：充斥着广告、情绪化发泄和无关噪音。

如果将这些原始文本直接喂给“投资组合经理 (Portfolio Manager)”或“投资法官 (Invest Judge)”（通常使用极其昂贵且聪明的模型，如 GPT-4o 或 Claude 3.5 Sonnet）：
1. **Token 成本极其昂贵**。
2. **上下文过载 (Lost in the middle)**：核心逻辑被大量的无效文字稀释，导致大模型抓错重点。

**引入“清洗与降噪层”后：**
系统会先使用一个极低成本、极快速度的“守门员模型”（如 `GPT-4o-mini`, `Gemini-1.5-Flash`，甚至国内极具性价比的 `DeepSeek`）对原始数据进行“脱水”。
它会滤除所有法律废话、广告和无关信息，仅提取核心的数据点和因果逻辑，再把高度浓缩的“干货”喂给主决策模型。

---

## 2. Proposed Architecture

### [MODIFY] default_config.py
在全局配置中新增清洗模型的配置：
```python
"scrubber_llm_provider": "openai",  # 建议使用最便宜快速的提供商
"scrubber_llm": "gpt-4o-mini",      # 承担粗活累活的低成本大模型
```

### [NEW] tradingagents/agents/utils/data_scrubber.py
新增一个 `DataScrubber` 独立模块。
- **功能**：接收任意长文本，调用 `scrubber_llm`，执行定制化的“脱水 Prompt”。
- **针对性 Prompt 示例**：
  *   **财报过滤**：“提取资产负债表异常变动、前瞻性指引（Forward Guidance）、以及明确的风险预警。舍弃所有法律免责声明。”
  *   **新闻过滤**：“将这 10 篇新闻提取为 3 条核心宏观/微观事件，每条不超过 50 字。”

### [MODIFY] Tool Functions (如 news_data_tools.py)
在工具链获取到原始文本后，将其通过 Scrubber 拦截处理后再返回给 Graph。
```python
def get_news(ticker, start_date, end_date):
    raw_news = interface.get_news(ticker, start_date, end_date)
    # 经过清洗层降噪
    scrubbed_news = DataScrubber.scrub_news(raw_news)
    return scrubbed_news
```

---

## 3. 远期收益 (Future Extensions for US Stocks)

拥有了这套强大的“漏斗过滤机制”后，我们就能安全地引入那些极其庞大但价值极高的数据源，而不用担心系统崩溃：
1. **SEC Edgar 接口接入**：自动抓取目标公司的最新 10-K，交由 Scrubber 浓缩。
2. **Seeking Alpha / Motley Fool 研报接入**：抓取华尔街大行的长篇研报，提取多空观点，喂给我们的 `bull_researcher` 和 `bear_researcher` 当作弹药！

---

## 4. User Review Required

> [!IMPORTANT]
> **API 调用次数增加**
> 虽然我们用的是便宜的模型来做清洗，但这会导致系统对 LLM 的 API 调用**频次增加**。
> 获取一条数据 = 调用 1 次 API 获取数据 + 调用 1 次大模型清洗 + 调用 1 次主模型做分析。

## 5. 落地建议

由于这层清洗机制严重依赖大模型的文本处理能力，在编写代码时，我们需要精确设计“脱水 Prompt（Scrubbing Prompts）”。建议第一步先在 `news_analyst`（新闻分析师）上进行试点，测试新闻被“脱水”后，主模型的分析质量是否有所提升。

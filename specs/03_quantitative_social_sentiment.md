# 03. 散户情绪量化指标 (Quantitative Social Sentiment)

## 1. 目标与价值 (Goal & Value)
原版框架中的社交情绪分析极其粗糙：直接去读最新的几篇新闻或 Twitter 帖子文本。大模型很容易被单篇极端的帖子带偏（噪音极大）。
借鉴优秀 Fork (BigA) 的思路，我们不应该让大模型去硬读文本，而是要**量化社交热度**，为美股建立一套硬性的情绪指标。

## 2. 改造方案 (Implementation Plan)
- **平台选择**：
  - **StockTwits**：美股最纯粹的散户论坛，每条消息自带 `$TICKER` 和明确的 `Bullish/Bearish` 标签。
  - **Reddit (r/wallstreetbets)**：提供话题热度榜单。
- **核心模块集成点**：
  - 彻底重构 `tradingagents/agents/analysts/social_media_analyst.py`。
  - 开发一个专门的 `StockTwits Monitor` 脚本（代替原有的纯文本搜索）。
  - 该脚本计算两个核心值：
    1. **热度指数 (Volume Z-Score)**：过去 24 小时讨论量相比历史均值的激增倍数。
    2. **多空比 (Bull/Bear Ratio)**：明确带标签的发帖中，看涨与看跌的比例。
  - 将这些**硬性数据**（例如：热度 95分，多空比 3.5:1）喂给大模型，而不是喂给它 50 篇杂乱的帖子。

## 3. 预期研报输出效果对比 (Expected Output)
- **原版输出**：“从最近的两篇帖子来看，大家觉得股票会涨，情绪偏向看多。”
- **升级后输出**：“该股目前在 StockTwits 上的讨论量激增（Z-Score > 3.0，进入散户极度狂热区间），且多空比达到惊人的 4:1。历史回测显示此阶段面临极高的逼空 (Short Squeeze) 或见顶回落风险，建议谨慎。”

## 4. 待确认问题 (Open Questions for You)
- StockTwits 存在免费 API 接口限制，我们可能需要使用第三方代理或非官方的爬虫手段，您是否接受这种方式？
- 您是否还有其他关注的美股社交平台（如 X/Twitter），需要一起纳入量化监控？

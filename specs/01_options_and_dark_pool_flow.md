# 01. 引入期权与暗池数据 (Options & Dark Pool Flow)

## 1. 目标与价值 (Goal & Value)
原版系统的 `Market Analyst` 和 `Trader` 主要依赖 Yahoo Finance 的基础 K 线数据（开高低收、成交量），这在美股市场中是远远不够的。美股的短期价格波动极大程度上受制于**机构资金流向 (Institutional Flow)**，具体体现在期权异动 (Unusual Options Activity) 和暗池大单 (Dark Pool Prints) 上。
通过引入这些数据，我们的系统可以在给出“入场价”和“止损价”时，具备极强的机构支撑逻辑。

## 2. 改造方案 (Implementation Plan)
- **数据源推荐**：
  - **Polygon.io**：提供全市场的期权链数据和实时交易流。
  - **Financial Modeling Prep (FMP)**：提供简化的期权异动监控和暗池交易摘要，性价比高。
  - **CBOE/Tradier**：提供免费的基础期权链 (Options Chain)。
- **核心模块集成点**：
  - 修改 `tradingagents/agents/utils/core_stock_tools.py`。
  - 新增工具：`get_options_flow(ticker, date)` 和 `get_put_call_ratio(ticker)`。
  - 将工具挂载给 `Market Analyst` 或 `Trader Agent`。

## 3. 预期研报输出效果对比 (Expected Output)
- **原版输出**：“价格已突破 50 日均线，呈现上升趋势，建议 150 美元买入。”
- **升级后输出**：“价格突破 50 日均线，且侦测到 150 美元行权价存在大量未平仓看跌期权 (Put Wall) 形成强力支撑，同时暗池出现 500 万美元级别大单买入。建议在 152 美元建仓，跌破 150 美元止损。”

## 4. 待确认问题 (Open Questions for You)
- 您目前是否有正在使用的美股高级数据 API 账号（如 Polygon.io 或 FMP）？
- 您希望主要关注 **Put/Call Ratio（看涨看跌情绪比）** 还是 **Unusual Options Activity（期权异动大单）**？

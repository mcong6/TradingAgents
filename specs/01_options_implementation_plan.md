# 整合美股期权数据与暗池思路 (yfinance 方案)

本计划旨在将 `yfinance` 提供的免费期权链数据接入系统，使 Market Analyst 和后续的 Trader 能够在技术面之上，参考**期权市场的情绪分布 (Put/Call Ratio)** 以及**支撑阻力区 (Options Walls)**，给出更精准的美股交易建议。

## Proposed Changes

### 1. Dataflows 层: 实现期权抓取逻辑

我们将在底层的 yfinance 数据流模块中，加入免费期权数据的获取与处理逻辑：

#### [MODIFY] [y_finance.py](file:///Users/mingzhecong/Documents/tradingagents/tradingagents/dataflows/y_finance.py)
- **新增函数** `get_options_data(ticker: str)`：
  1. 通过 `yf.Ticker.options` 自动获取最近的期权到期日。
  2. 获取看涨 (Call) 和看跌 (Put) 期权链。
  3. 计算总的 **Put/Call Ratio (PCR)**。
  4. 寻找资金最密集的行权价（Open Interest 最大的 Strike Price），定义为 **Call Wall (潜在阻力)** 和 **Put Wall (潜在支撑)**。
  5. 将结果格式化为易读的 Markdown 文本供大模型分析。

### 2. Interface 层: 注册新工具

我们需要将新开发的期权工具注册到系统的路由表和供应商池中：

#### [MODIFY] [interface.py](file:///Users/mingzhecong/Documents/tradingagents/tradingagents/dataflows/interface.py)
- 将 `"get_options_data"` 注册到 `TOOLS_CATEGORIES["core_stock_apis"]["tools"]` 中。
- 在 `VENDOR_METHODS` 字典里添加对应的路由：`"get_options_data": {"yfinance": get_options_data_yfinance}`。

### 3. Utils 层: 暴露工具接口

我们需要在 Agent 的公共工具层注册 LangChain 格式的 `@tool`：

#### [MODIFY] [core_stock_tools.py](file:///Users/mingzhecong/Documents/tradingagents/tradingagents/agents/utils/core_stock_tools.py)
- 添加 `@tool` 函数 `get_options_data(symbol: str)`，通过 `route_to_vendor` 转发。

#### [MODIFY] [agent_utils.py](file:///Users/mingzhecong/Documents/tradingagents/tradingagents/agents/utils/agent_utils.py)
- 将新工具加入到 `__all__` 列表，供整个图系统导入。

### 4. Agent 层: 武装 Market Analyst

最后，将这个新武器交给负责市场技术分析的 Agent：

#### [MODIFY] [trading_graph.py](file:///Users/mingzhecong/Documents/tradingagents/tradingagents/graph/trading_graph.py)
- 在 `_create_tool_nodes` 中，把 `get_options_data` 加给 `market` 工具节点。

#### [MODIFY] [market_analyst.py](file:///Users/mingzhecong/Documents/tradingagents/tradingagents/agents/analysts/market_analyst.py)
- 在 `market_analyst_node` 内导入 `get_options_data` 并加入到 `tools` 列表中。
- **修改系统提示词 (system_message)**：引导 Agent 在给出行情判断时，必须参考 `get_options_data` 返回的支撑阻力位 (Put/Call Wall) 和市场情绪 (PCR)。

---

## Verification Plan

1. **自动测试验证**：编写一个临时脚本，直接调用 `get_options_data_yfinance("AAPL")`，确保正确返回最近一期的期权链总结、PCR 以及支撑/阻力价位。
2. **端到端流程验证**：拉起整个图结构测试一只美股（如 AAPL 或 TSLA），检查 `Market Analyst` 是否调用了 `get_options_data`，且生成的报告里是否融合了期权面的数据逻辑。

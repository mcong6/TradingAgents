# 衍生宏观指标扩展计划与 FMP 数据源展望

## 1. 未来 FMP (Financial Modeling Prep) 数据源展望
针对前文提到的那些因为 FRED 缺乏数据而未能加入的指标，FMP API 恰好能够完美填补其中的部分空白。如果未来集成 FMP，我们可以直接获取以下高价值的华尔街指标：
*   **股权风险溢价 (Equity Risk Premium, ERP)**：FMP 提供了专门的 `/api/v4/market_risk_premium` 接口，可以直接按国家/市场获取实时的 ERP。
*   **远期盈利收益率 (Forward Earnings Yield)**：FMP 的 `/api/v3/key-metrics` 接口提供了 Earnings Yield 数据，同时通过结合分析师预期 (Analyst Estimates API)，可以直接计算出远期收益率。
*   **部分宏观经济领先指标 (如 PMI/ISM 等)**：FMP 的经济日历和宏观 API 涵盖了比 FRED 更贴近实盘交易的高频经济数据。

*(注：MOVE 指数和 CDX 属于极其昂贵的专有商业数据，即便在 FMP 中通常也无法获取，这些需要专业彭博终端。Zweig 宽度推力则可以通过拉取 FMP 的全市场股票涨跌分布自行写公式回溯计算。)*

---

## 2. 衍生合成指标实施计划 (User Review Required)

> [!IMPORTANT]  
> FRED 上最缺乏的是**美日利差 (U.S.-Japan Yield Spread)**（因为 FRED 没有日本国债的**日度**数据，只有滞后的月度数据）。强行用月度数据计算利差对 Agent 交易没有实战意义。
> 
> 因此，本次代码修改将**专注实现报告中最重要的、且 FRED 数据完备的“美联储净流动性 (Fed Net Liquidity)”**。

我们将修改 `tradingagents/dataflows/fred.py`，为其增加衍生指标的计算逻辑。

### [MODIFY] [fred.py](file:///Users/mingzhecong/Documents/tradingagents/tradingagents/dataflows/fred.py)
**计划变更内容**：
1. 在 `MACRO_SERIES` 中直接注册别名 `"fed_net_liquidity"`，映射到一个特殊标记 `"SYNTHETIC_FED_LIQUIDITY"`。
2. 修改 `get_macro_data()` 函数，拦截这个特殊标记。
3. **计算公式实现**：
   * 分别调用 FRED API 获取 `WALCL` (总资产, 每周更新, 单位: 百万美元)、`WTREGEN` (TGA, 每周更新, 单位: 百万美元)、`RRPONTSYD` (隔夜逆回购, 每日更新, 单位: 十亿美元)。
   * **数据对齐与单位转换**：由于更新频率不同，我们将采用**前向填充 (Forward-fill)** 逻辑，将每周更新的值填充到每日，以便与日度的逆回购数据对齐。逆回购的单位将乘以 1000 转换为百万美元。
   * **净流动性 = WALCL - WTREGEN - (RRPONTSYD * 1000)**。
4. 返回与原生 FRED 数据格式完全一致的 Markdown 报告，供 Agent 顺滑使用。

## 3. Verification Plan
- 编写测试脚本调用 `get_macro_data('fed_net_liquidity', ...)`。
- 确认脚本能正确并发拉取三个底层指标、正确前向填充日期、正确进行单位换算并得出净流动性数值。
- 确认输出格式包含 `**Latest:**` 和近期的历史数值表格。

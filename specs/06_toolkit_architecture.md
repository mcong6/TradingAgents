# 引入在线与离线冷热分离机制 (Online vs Offline Toolkit)

您说得非常对！我刚才犯了一个低级错误，没有仔细查看您项目根目录下的 `researchers` 文件夹。**您的代码库（源自 TauricResearch）不仅已经具备了多空辩论机制，甚至可以说是这套架构的原作核心！** 

既然辩论机制我们已经有了，接下来最值得我们借鉴的工程化改进就是 **Online vs Offline Toolkit (在线与离线工具箱冷热分离)**。

## 1. Goal & Value (目标与价值)

目前您的系统所有的工具（比如查新闻、查股票数据、甚至查刚才加的期权数据）都会直接通过网络调用 API。
如果您只是偶尔分析一两只股票，这没问题。但如果您想**测试您的系统在 2022 年底暴跌时的表现（回测）**，并在几百个历史交易日上运行多智能体，纯在线调用会导致：
1. **API 费用爆炸**（大模型费用 + 付费数据源 API 费用）。
2. **极速触发 Rate Limit**（比如 Yahoo Finance 会封 IP）。
3. **数据不一致**（部分在线 API 无法准确获取特定历史日期的“当天快照”）。

引入冷热分离后：
- 在 `default_config.py` 里设置 `online_tools = False`，系统进入**“纯离线回测模式”**。所有 Agent 的工具自动切换为离线版本（仅从本地缓存/数据库读取历史数据）。
- 设置 `online_tools = True`，系统进入**“实盘在线模式”**，实时抓取最新数据。

---

## 2. Proposed Changes

### [MODIFY] default_config.py
在全局配置中新增开关：
```python
"online_tools": os.getenv("TRADINGAGENTS_ONLINE_TOOLS", "True").lower() == "true",
```

### [MODIFY] agent_utils.py
1. 引入 `Toolkit` 面向对象类封装。
2. 将原本散落的工具（如 `get_stock_data`, `get_options_data` 等）全部改为 `Toolkit` 的静态方法。
3. 针对高频数据接口，提供两套实现：
   - `get_stock_data_online`: 强制请求远端 API，并将结果保存到本地缓存 (`data_cache/` 目录)。
   - `get_stock_data`: 强制只读取本地缓存，如果找不到直接返回错误，防止偷偷跑网络请求。

### [MODIFY] Analyst 节点重构
修改 `tradingagents/agents/analysts/` 下的各个分析师（如 `market_analyst.py`）：
在生成 `tools` 列表时，加入逻辑判断：
```python
def market_analyst_node(state: AgentState, toolkit: Toolkit):
    if toolkit.config["online_tools"]:
        tools = [toolkit.get_stock_data_online, toolkit.get_options_data_online, ...]
    else:
        tools = [toolkit.get_stock_data, toolkit.get_options_data, ...]
    # ...
```

### [MODIFY] trading_graph.py
1. 在图构建初始化时，实例化 `self.toolkit = Toolkit(config=self.config)`。
2. 调整传入 Analyst 节点的方式，使它们能访问当前的 `toolkit`。

---

## 3. User Review Required

> [!IMPORTANT]
> **重构范围较广**
> 这个改造会触及所有的 Analyst 节点和 Tool 定义，属于“牵一发而动全身”的底层架构升级。

## 4. Open Questions

> [!WARNING]
> 对于本地数据缓存的存放形式，您倾向于哪种？
> 1. **纯 CSV / JSON 文件存储**（最简单，存放在 `dataflows/data_cache/` 文件夹下，不用装数据库）。
> 2. **MongoDB / SQLite 数据库存储**（更规范，但需要您在电脑上安装/启动数据库）。
> 建议初期先采用方案 1（纯文件存储），即插即用。您同意吗？

## 5. Verification Plan
1. 将 `online_tools` 设为 `True`，运行一次 AAPL，验证 `data_cache` 文件夹中生成了数据缓存。
2. 断开电脑网络，并将 `online_tools` 设为 `False`，再次运行 AAPL 的同一个日期，验证程序能纯离线秒出数据，而不会报错。

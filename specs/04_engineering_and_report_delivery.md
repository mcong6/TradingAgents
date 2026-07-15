# 04. 工程化输出与性能监控 (Engineering & Report Delivery)

## 1. 目标与价值 (Goal & Value)
“优秀的研报必须有优秀的卖相。”
即便我们做出了顶级深度的分析，如果最终输出只是一堆在命令行里滚动的黑白 Markdown 文本，它作为“参考价值”的观感依然是大打折扣的。
借鉴 `hkwsg` 和 `MarkLo127` 的做法，我们需要在基础分析流程之上，加上**成本控制**和**自动化、高颜值的交付通道**。

## 2. 改造方案 (Implementation Plan)
- **Graph 性能监控 (APM & Token Tracker)**：
  - 引入类似于 Fork 仓库中的 `perf_callbacks.py`。
  - 在每一次 LangGraph 节点运行完后，后台统计：耗时 (s)、输入 Token 数、输出 Token 数、折算成本 ($)。
  - 这对于美股分析极为重要，因为美股深度数据（财报、期权链）文本量大，防止 API 费用失控。
- **渲染器 (Render Layer)**：
  - 在 `Portfolio Manager` 做出最终决策后，新增一个步骤：**导出精美文档**。
  - 可以利用 Python 的 `docx` 或 `Jinja2 + WeasyPrint`，将 Markdown 报告一键转换为格式工整的 **Word 研报** 或 **PDF 投资卡片**。
- **自动化交付 (Automated Push)**：
  - 编写一个 `cron` 调度脚本（或通过 Python `schedule` 库），在每天美东时间早盘前（例如早上 8:30 EST）自动拉起程序。
  - 运行完毕后，将 PDF 报告自动发送到您的 **Slack、Discord 频道或个人 Email**。

## 3. 预期研报输出效果对比 (Expected Output)
- **原版输出**：需要手动运行 `python main.py --ticker AAPL`，然后去文件夹里翻找纯文本 `.md` 文件。
- **升级后输出**：每天早晨喝咖啡时，手机的 Slack 自动收到一份带有精美排版、图表和结论的 `AAPL 深度研报.pdf`，并在结尾附带了一句：“本次分析共耗时 45 秒，消耗模型成本 $0.03”。

## 4. 待确认问题 (Open Questions for You)
- 在报告分发方面，您日常习惯使用的接收端是什么？（Email, Slack, Telegram, Discord, 微信/飞书？）
- 报告格式上，您更倾向于传统的 Word / PDF，还是轻量级的 HTML 投资卡片截图？
- 您是否需要我们将 Token 消耗的统计日志直观地显示在报告末尾？

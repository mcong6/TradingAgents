# 引入 Obsidian 知识库与 RAG 记忆检索体系

本计划旨在借鉴 `jiwoomap/TradingAgents-Dashboard` 的优秀设计，将基于向量数据库（ChromaDB）的 RAG（检索增强生成）与本地 Obsidian 知识库结合，让多智能体系统具备“长期记忆”和“自我进化”能力。

## 1. Goal & Value (目标与价值)

对于美股市场，财报季、美联储议息会议等周期性事件不断重演。
如果每次 Agent 都是“从零开始”分析，会错失历史上下文。引入这套机制后：
- **历史回溯 (RAG)**：在分析 AAPL 时，Agent 会自动从 ChromaDB 中检索出**上个季度或者去年同样遇到“加息预期升温”时的分析报告**，作为决策参考。
- **本地知识注入 (Obsidian)**：您可以自己建立一个 Obsidian 笔记本，写下您的私人美股交易法则（比如：“标普500 VIX > 30 时不盲目抄底”）。Agent 在运行前会读取并将其化为它的核心行为准则。

---

## 2. Proposed Changes

我们将分为两个核心步骤来改造您的代码库：

### [MODIFY] [memory.py](file:///Users/mingzhecong/Documents/tradingagents/tradingagents/agents/utils/memory.py)

借鉴 Fork 仓库，彻底改造 `FinancialSituationMemory` 类（或新建一个 `KnowledgeBaseMemory` 类）：
1. **集成 ChromaDB**：引入 `chromadb.PersistentClient` 替代原有的短效内存，将记忆持久化到本地 `./chroma_db` 文件夹。
2. **新增 `load_from_obsidian(vault_path)`**：
   - 遍历指定的 Obsidian 文件夹（如 `~/Documents/Obsidian/TradingAgents/`）下所有的 `.md` 格式笔记。
   - 以 `笔记标题 + 前300字摘要` 作为向量化 (Embedding) 的输入文本 (Query context)。
   - 以 `笔记全文` 作为大模型的背景知识 (Metadata/Document)。
3. **新增 `save_to_obsidian(content, filename)`**：
   - 每次生成完整的每日研报后，不光在终端输出，还自动排版并保存到您的 Obsidian 文件夹中，方便您查阅、修改并作为以后的养料。

### [MODIFY] [trading_graph.py](file:///Users/mingzhecong/Documents/tradingagents/tradingagents/graph/trading_graph.py)

调整主图结构的运行生命周期，打通记忆库：
1. **启动阶段 (Init)**：在拉起 Agent 前，调用 `load_from_obsidian`，自动把您新写的私人笔记更新到 ChromaDB。
2. **Agent 分析阶段 (Pre-process)**：把当前的宏观背景（如：当前美联储利率、期权墙状态）输入给 ChromaDB，提取最相关的 3 篇历史报告/笔记。通过 `SystemMessage` 强行喂给 `Portfolio Manager`。
3. **结束阶段 (Post-process)**：将当天的分析结果调用 `save_to_obsidian` 存回知识库，形成记忆闭环。

---

## 3. User Review Required

> [!IMPORTANT]
> **依赖项增加**
> 我们需要在 `requirements.txt` 中添加 `chromadb` 库来实现向量检索。如果您在部署环境中对此有限制，请告知。

## 4. Open Questions

> [!WARNING]
> 为了实现将报告写入您的本地 Obsidian，我们需要知道：
> **您电脑上 Obsidian 笔记库 (Vault) 的具体绝对路径是什么？** 
> 比如：`/Users/mingzhecong/Documents/Obsidian/TradingNotes/`
> （如果您还没用过 Obsidian，我们也可以先指定一个默认文件夹，比如 `tradingagents/knowledge_base/`，后期您可以直接用 Obsidian 打开这个文件夹。）

## 5. Verification Plan

1. **写操作测试**：写一个脚本生成一篇假报告，确认它能正确在您的 Obsidian 目录下生成对应的 `.md` 文件。
2. **读与向量测试**：手动在 Obsidian 里写一句假笔记：“当AAPL的Put/Call Ratio大于1.5时，必须清仓”。然后用脚本跑一遍 `get_memories`，看看 ChromaDB 能否根据上下文精准命中这条规则。

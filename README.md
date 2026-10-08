# AI Data Agent

> 一个面向 **AI Data / AI Agent Platform / AI Infra** 的工程实践项目，探索如何从传统的 LLM 应用逐步构建一个具备 **Planner、DAG 调度、Task Agent、Tool Runtime、MCP、RAG、LLM Cache、Observability** 能力的 AI Agent 系统。

AI Data Agent 是一个面向数据分析场景的 AI Agent。

用户可以通过自然语言提出数据分析问题，系统会经过 **意图识别 → 任务规划 → DAG 调度 → Task Agent 执行 → Tool Calling → 数据分析 → 结果汇总**，最终生成自然语言分析结果。

与简单的 **Text-to-SQL** 应用不同，本项目更关注 AI Agent 背后的工程问题：

* 如何让 LLM 负责决策，而不是直接控制系统
* 如何将复杂问题拆解成可执行任务
* 如何构建任务依赖关系
* 如何并行执行独立任务
* 如何让不同 Task 之间复用中间结果
* 如何管理 Tool
* 如何通过 MCP 接入外部能力
* 如何实现 RAG
* 如何缓存 LLM 请求
* 如何统计 Token、Cost、Latency
* 如何构建 Agent Runtime
* 如何进一步演进为 Agent Platform

---

# ✨ 项目特点

当前项目已经实现：

* **LLM Intent Router**
* **LLM Planner**
* **Task DAG**
* **DAG Scheduler**
* **Parallel Task Execution**
* **Task Agent**
* **Tool Calling**
* **PostgreSQL Text-to-SQL**
* **SQL 安全校验**
* **Result Store**
* **Result Reuse**
* **Result Profiling**
* **Anomaly Detection**
* **Chart Generation**
* **Production-oriented RAG**
* **MCP Server / Client**
* **LLM Cache**
* **Redis Cache Backend**
* **Execution Trace**
* **Metrics Collector**
* **Token / Cost / Latency Tracking**
* **LangGraph Agent Orchestration**

项目的核心目标不是简单实现一个 Chatbot，而是逐步构建一个真正的 **Agent Runtime**。

---

# 🏗️ 系统架构

整体架构如下：

```text
                         User
                          │
                          ▼
                  ┌──────────────┐
                  │ LLM Router   │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │   Planner    │
                  └──────┬───────┘
                         │
                       Task DAG
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
           Task Agent  Task Agent  Task Agent
              │          │          │
              └──────────┼──────────┘
                         ▼
                  ┌──────────────┐
                  │ Tool Runtime │
                  └──────┬───────┘
                         │
        ┌────────────────┼─────────────────┐
        ▼                ▼                 ▼
   SQL Tool          RAG / MCP        Analysis Tools
        │
        ▼
   PostgreSQL
        │
        ▼
  Result Store
        │
        ▼
   Final Answer
```

整个系统主要分为：

```text
Router
  ↓
Planner
  ↓
DAG Scheduler
  ↓
Task Agent
  ↓
Tool Runtime
  ↓
Data / RAG / MCP
  ↓
Result Store
  ↓
Summary
```

---

# 🧠 Agent 执行流程

一次完整的 Agent 请求大致经过：

```text
用户问题
   │
   ▼
Intent Routing
   │
   ▼
Task Planning
   │
   ▼
生成 Task DAG
   │
   ▼
依赖关系解析
   │
   ▼
获取 Ready Tasks
   │
   ▼
Task Agent
   │
   ▼
LLM Tool Calling
   │
   ▼
Tool Runtime
   │
   ▼
Tool Result
   │
   ▼
Result Store
   │
   ▼
执行下游 Task
   │
   ▼
Final Summary
```

与传统的：

```text
Question
   ↓
SQL
   ↓
Answer
```

相比，本项目采用：

```text
Question
   ↓
Understanding
   ↓
Planning
   ↓
DAG Execution
   ↓
Tool Calling
   ↓
Data Processing
   ↓
Result Reuse
   ↓
Synthesis
```

因此可以处理更加复杂的多步骤数据分析任务。

---

# 🧩 核心组件

## 1. Router

Router 负责判断用户请求的高层意图。

当前主要包含：

```text
data_query
knowledge
analysis
system
```

Router 不负责真正执行任务，而是负责确定：

> **这个请求应该进入哪类 Agent 工作流？**

---

# 2. Planner

Planner 将用户的自然语言需求转换成结构化 Task DAG。

一个 Task 通常包含：

```text
task_id
description
dependencies
required_tools
expected_output
```

例如：

```text
T1: 查询整体销售额
 │
 ├──────────────┐
 ▼              ▼
T2             T3
按类别统计      按时间统计
 │              │
 └──────┬───────┘
         ▼
        T4
    分析类别增长
         │
         ▼
        T5
    异常检测
         │
         ▼
        T6
    生成最终结论
```

Planner 主要负责：

* 复杂问题拆解
* Task 依赖分析
* 识别可以并行执行的 Task
* 避免重复任务
* 复用已有结果
* Progressive Drill-down
* 构建可执行 DAG

---

# 3. Task Agent

Task Agent 负责执行 Planner 分配的单个 Task。

其基本执行流程：

```text
Task
 │
 ▼
LLM
 │
 ├── Tool Call
 │      │
 │      ▼
 │   Tool Runtime
 │      │
 │      ▼
 │   Tool Result
 │      │
 └──────┘
 │
 ▼
Task Result
```

这里有一个重要的设计：

```text
Planner
   ↓
决定“做什么”

Task Agent
   ↓
决定“这个 Task 怎么执行”

Tool Runtime
   ↓
负责真正执行操作
```

因此 Planner、Task Agent 和 Tool Runtime 是相互解耦的。

---

# 4. DAG Scheduler

Planner 生成 DAG 后，由 Scheduler 根据依赖关系决定哪些 Task 可以执行。

例如：

```text
          T1
        /    \
       ▼      ▼
      T2      T3
       \      /
        ▼    ▼
          T4
```

执行过程：

```text
T1
 ↓
T2 + T3
 ↓
T4
```

其中：

```text
T2
T3
```

之间没有依赖关系，因此可以并行执行。

这种执行模型与传统大数据系统中的 DAG Scheduler 非常类似。

---

# 5. Parallel Execution

独立 Task 支持并行执行。

例如：

```text
             Planner
                │
        ┌───────┼───────┐
        ▼       ▼       ▼
       T1      T2      T3
        │       │       │
        └───────┼───────┘
                ▼
               T4
```

T1、T2、T3 可以同时执行。

执行模型：

```text
DAG
 ↓
Dependency Resolution
 ↓
Ready Queue
 ↓
Parallel Workers
 ↓
Task Completion
 ↓
Unlock Dependent Tasks
```

这部分可以直接类比传统分布式计算系统中的：

```text
DAG Scheduler
Dependency Management
Task Scheduling
Parallel Execution
```

但 Agent 系统额外增加了一个重要因素：

> Task 的执行决策可能来自 LLM，因此 Runtime 需要对 LLM 的不确定性进行约束。

---

# 🔧 Tool Runtime

Tool Runtime 是 Agent 真正执行外部操作的地方。

当前支持：

| Tool             | 功能           |
| ---------------- | ------------ |
| `run_sql`        | 执行 SQL       |
| `get_schema`     | 获取数据库 Schema |
| `profile_result` | 分析查询结果       |
| `detect_anomaly` | 异常检测         |
| `generate_chart` | 生成图表         |

执行流程：

```text
LLM
 ↓
Tool Call
 ↓
Tool Router
 ↓
Specific Tool
 ↓
Execution
 ↓
Result Store
 ↓
result_id
```

Task Agent 不需要直接操作数据库或其他基础设施。

---

# 🗄️ PostgreSQL

项目使用 PostgreSQL 作为主要结构化数据存储。

数据模型：

```text
users
products
orders
```

其中 `orders` 表包含：

```text
id
user_id
product_id
amount
status
order_time
```

项目构造了约 **100 万条订单数据**，用于模拟真实的数据分析场景。

系统通过自然语言生成 SQL：

```text
Natural Language
       ↓
     LLM
       ↓
   SQL Generation
       ↓
 SQL Validation
       ↓
 PostgreSQL
       ↓
 Query Result
```

---

# 🔐 SQL 安全控制

由于 SQL 是由 LLM 自动生成的，因此系统不能直接允许 LLM 执行任意 SQL。

当前实现了：

* SELECT-only
* 单 SQL Statement
* DML 禁止
* DDL 禁止
* SQL 长度限制
* Query Timeout
* Result Row Limit
* Read-only Database User

禁止：

```sql
INSERT
UPDATE
DELETE
DROP
ALTER
CREATE
TRUNCATE
```

数据库权限层面同时使用独立的只读用户执行 AI 生成的 SQL。

> 当前 SQL Validator 主要用于工程实践和学习，并不是完整的生产级 SQL Security Boundary。生产环境还需要进一步结合数据库权限隔离、Resource Quota、Query Governance、Sandbox 等机制。

---

# 📦 Result Store

Agent 系统中的 Task 可能产生大量中间数据。

因此项目没有简单地把所有结果直接塞进 LLM Context。

采用：

```text
Task A
  │
  ▼
Result Store
  │
  ▼
result_id
  │
  ▼
Task B
```

而不是：

```text
Task A
  │
  ▼
Huge Result
  │
  ▼
LLM Context
```

这种设计可以减少：

* Context Token 消耗
* 重复计算
* 重复查询

同时为后续实现：

* Result Reuse
* Result Cache
* Large Result Management
* State Management

提供基础。

---

# 📊 数据分析能力

## Result Profiling

可以对查询结果进行：

* Column 分析
* Null Count
* 数据类型分析
* 基础统计
* Sample Values

---

## Anomaly Detection

当前实现基于统计方法进行异常检测。

基本流程：

```text
Query Result
     ↓
Statistical Analysis
     ↓
Anomaly Detection
     ↓
Anomaly Candidates
     ↓
LLM Explanation
```

---

## Chart Generation

Chart Tool 支持：

* X Column
* Multiple Y Columns
* Title
* X Label
* Y Label

Agent 可以根据分析结果生成可视化图表。

---

# 🔎 RAG

项目同时实现了一套面向真实文档的 RAG Pipeline。

整体流程：

```text
PDF
 │
 ▼
PDF Parser
 │
 ▼
Document Model
 │
 ▼
Structure Classification
 │
 ▼
Structure-aware Chunking
 │
 ▼
Embedding
 │
 ▼
pgvector
 │
 ▼
Vector Retrieval
 │
 ▼
LLM
```

文档数据主要包含：

```text
Document
Chunk
Metadata
Embedding
```

并存储在 PostgreSQL / pgvector 中。

当前已经完成真实 PDF 的：

```text
PDF
 ↓
Parsing
 ↓
Chunking
 ↓
Embedding
 ↓
pgvector
 ↓
Vector Retrieval
```

完整链路。

---

# 🔌 MCP

项目集成了 **Model Context Protocol（MCP）**。

MCP 用于将外部能力以标准化方式暴露给 Agent。

整体结构：

```text
AI Application / Agent Runtime
             │
             ▼
         MCP Client
             │
             ▼
        MCP Protocol
             │
             ▼
         MCP Server
             │
             ▼
       External System
```

当前 MCP Server 提供：

```text
get_schema
run_sql
```

Agent 可以通过 MCP Client：

```text
发现 Tool
   ↓
获取 Tool Schema
   ↓
转换成 LLM Tool Definition
   ↓
LLM 选择 Tool
   ↓
MCP Client
   ↓
MCP Server
   ↓
External System
```

这样可以将：

```text
Agent Runtime
```

与：

```text
External Tools
```

进行解耦。

---

# 🧠 LangGraph

项目使用 LangGraph 作为 Agent Workflow 的编排层。

核心 Graph：

```text
START
  ↓
Router
  ↓
Planner
  ↓
DAG Scheduler
  ↓
Task Execution
  ↓
Check Completed Tasks
  │
  ├── Continue ──→ Task Execution
  │
  └── Done ──────→ Summary
                         ↓
                        END
```

LangGraph 在这里主要负责：

* State 管理
* Workflow 编排
* Conditional Routing
* Execution Loop

而具体的：

```text
Planner
TaskRunner
Tool Runtime
DAG Scheduler
Result Store
```

仍然由项目自己实现。

因此 LangGraph 更像是：

> **Agent Workflow Orchestration Layer**

而不是整个 Agent Runtime。

---

# 💾 LLM Cache

LLM 请求通常具有较高的：

* Latency
* Cost

因此项目实现了 LLM Cache。

整体结构：

```text
TaskRunner
    │
    ▼
 LLM Cache
    │
    ├── HIT
    │    │
    │    ▼
    │ Cached Response
    │
    └── MISS
         │
         ▼
        LLM
         │
         ▼
       Cache
```

Cache 抽象：

```text
LLMCache
   │
   ▼
CacheBackend
   ├── InMemoryBackend
   └── RedisBackend
```

当前支持：

* SHA256 Cache Key
* TTL
* LRU
* In-Memory Cache
* Redis Cache
* Cache Hit Tracking
* Cache Latency Tracking

通过抽象 `CacheBackend`，Agent Runtime 不需要关心底层使用的是：

```text
Memory
```

还是：

```text
Redis
```

---

# 📈 Observability

Agent 系统和传统 Web 服务相比，更难进行问题定位。

一次用户请求可能产生：

```text
LLM
 ↓
Tool
 ↓
LLM
 ↓
Tool
 ↓
LLM
 ↓
Task
 ↓
Task
```

因此项目实现了 Execution Trace。

当前事件类型包括：

```text
TASK_START
LLM_RESPONSE
LLM_CACHE_HIT
TOOL_CALL
TOOL_RESULT
TASK_END
TASK_ERROR
```

同时记录：

```text
Task
LLM Call
Tool Call
Latency
Token
Cost
Success / Failure
Error
```

---

# 📊 Metrics

Metrics Collector 当前统计：

```text
Tasks
├── total
├── success
└── failed

LLM
├── calls
├── cache_hits
├── cache_hit_rate
├── input_tokens
├── output_tokens
├── total_tokens
├── cost
└── avg_latency

Tools
└── tool usage
```

例如：

```text
Tasks
  total:       1
  success:     1
  failed:      0

LLM
  calls:       1
  cache hits:  0
  tokens:      2129
  cost:        0.004537
  latency:     4.698s
```

这些指标为后续构建：

```text
Agent Observability
Cost Control
Performance Optimization
Model Routing
```

提供基础。

---

# 🧱 Agent Runtime

从整体上看，目前项目已经具备一个简化版 Agent Runtime。

可以抽象成：

```text
                    Agent Runtime
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
     Planner         Task Runner       Tool Runtime
        │                │                │
        ▼                ▼                ▼
      Task DAG       LLM Calling      External Tools
                         │
                         ▼
                    Result Store
                         │
                         ▼
                  Execution Trace
                         │
                         ▼
                      Metrics
```

其中：

```text
Planner
```

负责：

> 做什么？

```text
Task Runner
```

负责：

> 怎么执行？

```text
Tool Runtime
```

负责：

> 如何真正执行外部操作？

```text
Result Store
```

负责：

> 中间结果存在哪里？

```text
Execution Trace / Metrics
```

负责：

> 系统到底执行了什么、耗费了多少资源？

---

# 🏢 Agent Platform 演进方向

项目的长期目标并不是停留在一个 Data Agent。

希望逐步演进为：

```text
                         Agent Platform
                               │
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                    ▼
    Agent Runtime        Model Gateway        Tool Gateway
          │                    │                    │
          │              ┌─────┴─────┐         ┌────┴────┐
          │              ▼           ▼         ▼         ▼
          │           DeepSeek      Qwen      MCP       APIs
          │
          ├── Planner
          ├── DAG Scheduler
          ├── Task Runtime
          ├── State / Memory
          ├── RAG
          ├── Cache
          ├── Observability
          ├── Security
          └── Cost Control
```

因此当前 Data Agent 实际上是整个 Agent Platform 的一个具体业务场景。

---

# 🗂️ 项目结构

```text
ai-data-agent/
│
├── app/
│   │
│   ├── agent/
│   │   └── planner_evaluator.py
│   │
│   ├── langgraph_demo/
│   │   ├── basic_graph.py
│   │   ├── router_graph.py
│   │   ├── llm_router_graph.py
│   │   ├── planner_graph.py
│   │   ├── dag_scheduler.py
│   │   └── parallel_executor.py
│   │
│   ├── rag/
│   │   ├── document_model.py
│   │   ├── pdf_parser.py
│   │   ├── structure_classifier.py
│   │   ├── chunk_model.py
│   │   ├── structure_chunker.py
│   │   ├── chunk_embedder.py
│   │   ├── document_ingester.py
│   │   └── vector_retriever.py
│   │
│   ├── tools/
│   │   ├── definitions.py
│   │   ├── router.py
│   │   ├── sql_tool.py
│   │   ├── schema_tool.py
│   │   ├── profile_tool.py
│   │   ├── anomaly_tool.py
│   │   └── chart_tool.py
│   │
│   ├── mcp/
│   │   ├── server.py
│   │   └── client.py
│   │
│   ├── planner.py
│   ├── task_agent.py
│   ├── task_runner.py
│   ├── result_store.py
│   ├── execution_trace.py
│   ├── metrics.py
│   ├── metrics_backend.py
│   ├── metrics_store.py
│   ├── metrics_registry.py
│   ├── cached_llm.py
│   ├── llm_cache.py
│   ├── cache_backend.py
│   ├── redis_backend.py
│   ├── db.py
│   ├── rag_db.py
│   ├── query.py
│   ├── schema.py
│   └── sql_validator.py
│
├── tests/
│
├── data/
│   └── documents/
│
├── docker-compose.yml
├── .env
├── .gitignore
└── README.md
```

---

# 🛠️ 技术栈

| 层级                  | 技术                       |
| ------------------- | ------------------------ |
| 编程语言                | Python                   |
| LLM                 | DeepSeek / Qwen          |
| Agent Orchestration | LangGraph                |
| Agent Protocol      | MCP                      |
| 关系数据库               | PostgreSQL               |
| 向量数据库               | pgvector                 |
| Cache               | Redis / In-Memory        |
| API                 | FastAPI                  |
| PDF Parsing         | PyMuPDF                  |
| SQL Driver          | psycopg2                 |
| DAG Execution       | ThreadPoolExecutor       |
| Observability       | ExecutionTrace + Metrics |
| Container           | Docker Compose           |
| 开发环境                | Windows / WSL2 / Linux   |

---

# 🚀 快速开始

## 环境要求

推荐：

```text
Python 3.11+
Docker Desktop
WSL2 / Linux
PostgreSQL
Redis
LLM API
```

Windows 用户推荐使用：

```text
Windows 11
+
WSL2
+
Ubuntu
+
Docker Desktop
```

---

## 1. Clone 项目

```bash
git clone https://github.com/liyaosket/ai-data-agent.git
cd ai-data-agent
```

---

## 2. 创建 Python 环境

```bash
python -m venv .venv
```

Linux / WSL2：

```bash
source .venv/bin/activate
```

Windows：

```powershell
.venv\Scripts\activate
```

安装依赖：

```bash
pip install -r requirements.txt
```

---

# 3. 配置环境变量

创建：

```text
.env
```

例如：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key

DASHSCOPE_API_KEY=your_dashscope_api_key
DASHSCOPE_BASE_URL=your_dashscope_base_url

QWEN_EMBEDDING_MODEL=qwen3.7-text-embedding
QWEN_EMBEDDING_DIMENSIONS=1024
```

不要将真实 API Key 提交到 Git。

---

# 4. 启动 PostgreSQL

项目使用 pgvector：

```bash
docker compose up -d postgres
```

检查：

```bash
docker ps
```

默认数据库：

```text
Database: ecommerce
User: dev
Port: 5432
```

---

# 5. 启动 Redis

```bash
docker compose up -d redis
```

检查：

```bash
docker ps
```

应该可以看到：

```text
ai-data-postgres
ai-data-redis
```

---

# ▶️ 运行项目

项目中的模块可以使用 Python Module 方式运行。

例如：

```bash
python -m app.test_runtime_metrics
```

运行测试：

```bash
pytest
```

项目测试覆盖：

* Planner
* DAG Scheduler
* Task Runner
* Parallel Execution
* RAG
* Vector Retrieval
* LLM Cache
* Metrics
* MCP

---

# 🔍 一个典型请求

例如用户提出：

```text
过去一个月哪个商品类别销售额最高？
并分析一下原因。
```

系统可能生成：

```text
1. Router
      ↓
   data_query / analysis

2. Planner
      ↓
   T1: 计算各类别销售额
   T2: 计算历史周期销售额
   T3: 比较增长率
   T4: 检测异常类别
   T5: 分析影响因素
   T6: 生成最终结论

3. DAG Scheduler
      ↓
   并行执行无依赖 Task

4. Task Agent
      ↓
   根据任务选择 Tool

5. SQL Tool
      ↓
   PostgreSQL

6. Result Store
      ↓
   保存中间结果

7. Downstream Tasks
      ↓
   复用 result_id

8. Summary
      ↓
   最终答案
```

---

# 🧪 Planner Evaluation

Planner 不只是生成一个“看起来合理”的计划，还实现了基础结构化评估。

当前评估指标：

```text
Task Count
Dependency Count
Maximum Parallelism
Critical Path Length
Dependency Validity
Duplicate Tasks
Redundant Tasks
Dependency Cycles
```

例如：

```text
Planner
  ↓
Generated DAG
  ↓
Structural Validator
  │
  ├── Dependency Valid
  ├── No Duplicate IDs
  ├── No Unknown Dependencies
  ├── No Self Dependency
  └── No Cycles
```

这使 Planner 从单纯的 Prompt 输出进一步变成可测试的系统组件。

---

# 🔐 安全设计

当前项目已经实现：

* Read-only Database
* SQL Validation
* SELECT-only
* Query Timeout
* Result Row Limit
* Environment-based Secrets
* Tool Execution Boundary

生产环境还需要进一步考虑：

```text
Authentication
Authorization
Tenant Isolation
Network Isolation
Resource Quota
Rate Limiting
Prompt Injection Defense
Tool Permission
Sandbox
Audit Log
Secret Management
Model Governance
Tool Governance
```

---

# 🎯 设计原则

## 1. LLM 不是 Runtime

LLM 负责：

```text
Reasoning
Planning
Decision Making
Tool Selection
```

Runtime 负责：

```text
Execution
Permission
State
Timeout
Resource Control
Caching
Observability
```

核心原则：

> **LLM 决定做什么，Runtime 决定能不能做以及怎么执行。**

---

## 2. Planner 与 Executor 分离

```text
Planner
   ↓
Plan

Executor
   ↓
Execute
```

这样可以提高：

* 可测试性
* 可观测性
* 可复现性
* 调度能力
* 并行能力
* 故障处理能力

---

## 3. 中间结果使用引用传递

不要直接把大量数据塞进 LLM Context。

推荐：

```text
Task
 ↓
Result Store
 ↓
result_id
 ↓
Downstream Task
```

而不是：

```text
Task
 ↓
Huge Result
 ↓
LLM Context
```

---

## 4. Framework 不应该隐藏核心概念

项目在使用 LangGraph、MCP 等框架之前，优先理解和实现底层概念：

```text
Planner
DAG Scheduler
Task Runner
Tool Runtime
Result Store
Execution Trace
LLM Cache
Metrics
```

然后再使用框架进行编排。

这样可以避免：

> 只会使用 Agent Framework，而不了解 Agent Runtime。

---

# 📚 项目涉及的核心知识

## Agent Engineering

```text
Agent Runtime
Planner
Task Agent
Tool Calling
DAG
Parallel Execution
Result Reuse
MCP
LangGraph
```

## Data Engineering

```text
PostgreSQL
Text-to-SQL
SQL Validation
Data Analysis
Anomaly Detection
Chart Generation
```

## RAG

```text
PDF Parsing
Structure-aware Chunking
Embedding
pgvector
Vector Retrieval
```

## AI Infrastructure

```text
LLM Gateway
LLM Cache
Redis
Token Accounting
Cost Tracking
Latency Tracking
Execution Trace
Metrics
```

## Distributed Systems

```text
DAG Scheduling
Dependency Management
Parallel Execution
Result Reuse
Timeout
Resource Control
Observability
Caching
```

---

# 🧭 Roadmap

当前项目及学习路线：

```text
[x] LangGraph
[x] MCP
[x] Production RAG
[x] AI Coding Agent Concepts
[x] Agent Platform Architecture

[ ] Skill / Prompt / Tool / Model Management
[ ] FastAPI AI Service
[ ] Kafka × AI
[ ] Flink × AI
[ ] Docker × AI
[ ] Kubernetes × AI
[ ] AI System Design
```

整体方向：

```text
Big Data
    +
Distributed Systems
    +
AI Agent
    +
AI Infrastructure
```

---

# 🚧 当前项目定位

本项目是一个：

> **AI Agent Runtime / AI Platform 工程实践项目**

而不是一个已经完全生产化的 SaaS 系统。

项目重点是通过一个真实的数据分析场景，逐步实现和理解：

```text
LLM Application
      ↓
Tool Calling
      ↓
Agent
      ↓
Planner
      ↓
DAG
      ↓
Parallel Execution
      ↓
MCP
      ↓
RAG
      ↓
Cache
      ↓
Observability
      ↓
Agent Runtime
      ↓
Agent Platform
```

部分组件为了降低复杂度进行了工程化简化，例如：

* SQL Validator
* Metrics Persistence
* Result Store
* Model Routing
* Security Policy
* Failure Handling

如果用于真正的生产环境，还需要进一步增加：

```text
Distributed State
Authentication
Authorization
Multi-tenancy
Resource Scheduling
Quota
Sandbox
Audit
Governance
High Availability
```

---

# 💡 为什么做这个项目？

项目最初的问题很简单：

> **如何让 AI 不只是生成一个 SQL，而是真正完成一个复杂的数据分析任务？**

随着实现逐步深入，问题演变成：

```text
如何让 LLM 进行任务规划？
        ↓
如何把计划转换成 DAG？
        ↓
如何调度 DAG？
        ↓
如何并行执行 Task？
        ↓
如何让 Task 调用 Tool？
        ↓
如何复用中间结果？
        ↓
如何控制 LLM Cost？
        ↓
如何进行 Observability？
        ↓
如何接入 MCP？
        ↓
如何构建 Agent Runtime？
        ↓
如何进一步演进成 Agent Platform？
```

因此，这个项目最终希望探索的是：

> **如何将传统 Big Data / Distributed Systems 的工程能力，与现代 AI Agent / AI Infrastructure 结合起来。**

---

# 👨‍💻 Author

**Liyaosket**

GitHub：

https://github.com/liyaosket/ai-data-agent

---

# ⭐ Star History

如果这个项目对你理解 **AI Agent、AI Data、Agent Runtime、AI Infra** 有帮助，欢迎 Star ⭐。


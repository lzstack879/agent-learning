# Agent Learning Lab

这是一个按 12 周路线逐步构建 Agent 工程能力的可运行仓库。每个周次目录对应一个可独立阅读的最小项目，公共实现位于 `src/agent_learning`，测试位于 `tests/`。

## 快速开始

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
uvicorn agent_learning.api:app --reload
```

可选能力按需安装：`pip install -e ".[agents,mcp,memory,observability]"`。

## 周次地图

- `week01_min_loop`：纯 Python async Agent Loop
- `week02_tools`：Pydantic 工具 schema、5 个工具和安全执行器
- `week03_mcp_server`：FastMCP 文件系统服务（无依赖时提供兼容核心）
- `week04_travel_planner`：LangGraph 旅行规划（含纯 Python fallback）
- `week05_memory`：工作、会话、长期记忆
- `week06_agentic_rag`：检索工具与查询改写
- `week07_multi_agent`：Supervisor 写作团队
- `week08_eval`：指标、对抗样例和可靠性报告模板
- `week09_deploy`：FastAPI 流式 API、输入防护、模型路由
- `week10_projects`：三个作品的架构与验收清单
- `week11_12_interview`：面试题、What/How/Why 和模拟记录模板

外部模型通过 `ModelAdapter` 注入；默认使用确定性的 `DemoModel`，因此测试不需要 API Key。

## 运行演示

```bash
python -m agent_learning.demo
docker compose up --build
```

MCP 服务默认使用 `ROOT_DIRECTORY` 作为沙箱根目录，禁止路径越界和超大写入。


# MCP 示例项目

本项目演示了 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 的基本用法，包含三种不同传输方式的 MCP 服务器实现，以及基于 LangChain 的 MCP 客户端调用示例。

## 项目结构

```
MCP/
├── mcp_server_stdio.py        # 基于 stdio 传输的 MCP 服务器
├── mcp_server_sse.py          # 基于 SSE 传输的 MCP 服务器
├── mcp_server_streamable.py   # 基于 Streamable HTTP 传输的 MCP 服务器
├── mcp_client.py              # LangChain MCP 客户端示例
└── requirements.txt           # 依赖清单
```

## 文件说明

### MCP 服务器

三个服务器均提供相同的 `get_today` 工具（返回当前日期 `YYYY-MM-DD` 格式），但使用不同的传输协议：

| 文件 | 传输方式 | 启动方式 |
|------|----------|----------|
| `mcp_server_stdio.py` | `stdio` | `python mcp_server_stdio.py` |
| `mcp_server_sse.py` | `sse` | `python mcp_server_sse.py`（监听 `127.0.0.1:8000/sse`） |
| `mcp_server_streamable.py` | `streamable_http` | `python mcp_server_streamable.py`（监听 `127.0.0.1:8000/mcp`） |

核心代码示例（以 stdio 方式为例）：

```python
from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("date_tool_stdio")

@mcp.tool()
def get_today():
    """返回当前的年月日，格式YYYY-MM-DD"""
    return datetime.now().strftime("%Y-%m-%d")

if __name__ == "__main__":
    mcp.run()
```

### MCP 客户端

`mcp_client.py` 使用 `langchain_mcp_adapters` 将 MCP 服务器连接到 LangChain Agent，实现 LLM 自动调用 MCP 工具。

核心流程：

1. 通过 `MultiServerMCPClient` 配置 MCP 服务器（支持同时连接多个服务器）
2. 调用 `client.get_tools()` 获取所有 MCP 工具
3. 将工具注入 LangChain Agent，与 LLM 模型协同工作

```python
client = MultiServerMCPClient({
    "date-tool-stdio": {
        "transport": "stdio",
        "command": "python",
        "args": ["d:\\PycharmProjects\\Agent\\MCP\\mcp_server_stdio.py"],
    },
})

tools = await client.get_tools()
agent = create_agent(model=llm, tools=tools)
result = await agent.ainvoke({"messages": [("user", "今天几号？")]})
```

## 环境要求

- Python >= 3.10
- 依赖包（`requirements.txt`）：

```
mcp>=1.28.1
langchain-openai
langchain-mcp-adapters
python-dotenv
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件，填入阿里云 DashScope API Key：

```env
DASHSCOPE_API_KEY=your_api_key_here
```

### 3. 启动 MCP 服务器（可选）

stdio 模式无需手动启动，客户端会自动拉起进程。SSE 和 streamable HTTP 模式需独立运行：

```bash
# SSE 模式
python mcp_server_sse.py

# Streamable HTTP 模式
python mcp_server_streamable.py
```

### 4. 运行客户端

```bash
python mcp_client.py
```

## 关键依赖

- **[mcp](https://pypi.org/project/mcp/)** — MCP 官方 Python SDK，提供服务器和客户端实现
- **[FastMCP](https://modelcontextprotocol.io/quickstart/server)** — MCP SDK 中的快速服务器框架，装饰器方式注册工具
- **[langchain-mcp-adapters](https://github.com/langchain-ai/langchain-mcp-adapters)** — LangChain 与 MCP 的适配器桥接
- **[DashScope](https://dashscope.aliyun.com/)** — 阿里云百炼平台（本项目使用 `qwen-plus` 模型）

## 参考资料

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [LangChain MCP Adapters](https://github.com/langchain-ai/langchain-mcp-adapters)

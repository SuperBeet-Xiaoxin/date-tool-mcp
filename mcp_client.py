from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# 1. 用你的 MCP 配置创建客户端
client = MultiServerMCPClient(
    {
        "date-tool-stdio": {
            "transport": "stdio",
            "command": "python",
            "args": ["d:\\PycharmProjects\\Agent\\MCP\\mcp_server_stdio.py"],
        },
        # "date-tool-sse": {"transport": "sse", "url": "http://127.0.0.1:8000/sse"},
        # "date-tool-streamable": {"transport": "streamable_http", "url": "http://127.0.0.1:8000/mcp"},
    }
)

async def main():
    tools = await client.get_tools()

    llm = ChatOpenAI(
        model="qwen-plus",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        temperature=0.3,
    )

    agent = create_agent(
        model = llm,
        tools = tools,
    )

    result = await agent.ainvoke({"messages": [("user", "用必应搜索查一下今天的人工智能新闻")]})

    print("\n最终回答:", result["messages"][-1].content)

asyncio.run(main())
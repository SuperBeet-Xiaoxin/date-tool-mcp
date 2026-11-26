from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("date-tool-see", host = "127.0.0.1", port = 8000)
@mcp.tool()
def get_today():
    """返回当前的年月日，格式YYY-MM-DD"""
    return datetime.now().strftime("%Y-%m-%d")

if __name__== "__main__":
    mcp.run(transport = "sse")

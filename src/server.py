# server.py
from mcp.server.fastmcp import FastMCP
from obsidian_client import ObsidianClient

client = ObsidianClient(vault_path="/path/to/vault")
# Use client methods...

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"
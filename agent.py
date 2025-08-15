# server.py
from fastmcp import FastMCP

mcp = FastMCP("HelloServer")

@mcp.tool
def greet(name: str) -> str:
    """Return a friendly greeting."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    # Expose the server via STDIO (what Smithery expects)
    mcp.run()

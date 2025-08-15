#!/usr/bin/env python3
"""
Simple MCP Server Example for Smithery Deployment
This server provides basic text processing tools for AI agents.
"""

import asyncio
import json
import sys
from typing import Any, Dict

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp import types


# Initialize the MCP server
server = Server("simple-text-tools")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="reverse_text",
            description="Reverse the order of characters in a text string",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to reverse"
                    }
                },
                "required": ["text"]
            }
        ),
        types.Tool(
            name="count_words",
            description="Count the number of words in a text string",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to count words in"
                    }
                },
                "required": ["text"]
            }
        ),
        types.Tool(
            name="to_uppercase",
            description="Convert text to uppercase",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to convert to uppercase"
                    }
                },
                "required": ["text"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent]:
    """Handle tool calls."""
    if arguments is None:
        arguments = {}

    if name == "reverse_text":
        text = arguments.get("text", "")
        reversed_text = text[::-1]
        return [types.TextContent(type="text", text=f"Reversed text: {reversed_text}")]
    
    elif name == "count_words":
        text = arguments.get("text", "")
        word_count = len(text.split())
        return [types.TextContent(type="text", text=f"Word count: {word_count}")]
    
    elif name == "to_uppercase":
        text = arguments.get("text", "")
        uppercase_text = text.upper()
        return [types.TextContent(type="text", text=f"Uppercase text: {uppercase_text}")]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Main entry point for the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="simple-text-tools",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())

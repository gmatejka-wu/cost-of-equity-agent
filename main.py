#!/usr/bin/env python3
"""
MarktTrendite API MCP Server
This server provides information about the marktrendite.ai CostofEquity API variables
and can fetch cost of equity data for analysis.
"""

import asyncio
import sys
from typing import Any
import aiohttp
import json

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp import types

# Initialize the MCP server
server = Server("marktrendite-api-info")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="get_api_variables",
            description="Get information about available variables in the marktrendite.ai CostofEquity API",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        ),
        types.Tool(
            name="fetch_cost_of_equity_data",
            description="Fetch cost of equity data from the marktrendite.ai API",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of records to return (default: 10, max: 100)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "additionalProperties": False
            }
        ),
        types.Tool(
            name="explain_variable",
            description="Get detailed explanation of a specific API variable",
            inputSchema={
                "type": "object",
                "properties": {
                    "variable": {
                        "type": "string",
                        "description": "The variable name to explain (isin, date, MV, ddm_3, rim_3, gewichtet_3)",
                        "enum": ["isin", "date", "MV", "ddm_3", "rim_3", "gewichtet_3"]
                    }
                },
                "required": ["variable"]
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

    if name == "get_api_variables":
        variables_info = """
# MarktTrendite.ai CostofEquity API Variables

The API returns financial data with the following variables:

**Basic Information:**
- `isin`: International Securities Identification Number (unique identifier for securities)
- `date`: Date of the data record (format: YYYY-MM-DD)
- `MV`: Market Value in millions (market capitalization)

**Cost of Equity Models:**
- `ddm_3`: Dividend Discount Model 3-year estimate (%)
- `rim_3`: Residual Income Model 3-year estimate (%)
- `gewichtet_3`: Weighted 3-year estimate (%) - combines DDM and RIM models

**API Endpoint:** https://api.marktrendite.ai/CostofEquity

The data covers European stocks including Austrian, German, Swiss, and other European markets.
        """
        return [types.TextContent(type="text", text=variables_info.strip())]
    
    elif name == "fetch_cost_of_equity_data":
        limit = arguments.get("limit", 10)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.marktrendite.ai/CostofEquity") as response:
                    if response.status == 200:
                        data = await response.json()
                        # Limit the results
                        limited_data = data[:limit] if isinstance(data, list) else [data]
                        
                        result = f"Fetched {len(limited_data)} records from MarktTrendite API:\n\n"
                        for i, record in enumerate(limited_data, 1):
                            result += f"**Record {i}:**\n"
                            result += f"- ISIN: {record.get('isin', 'N/A')}\n"
                            result += f"- Date: {record.get('date', 'N/A')}\n"
                            result += f"- Market Value: {record.get('MV', 'N/A')} million\n"
                            result += f"- DDM 3-year: {record.get('ddm_3', 'N/A')}%\n"
                            result += f"- RIM 3-year: {record.get('rim_3', 'N/A')}%\n"
                            result += f"- Weighted 3-year: {record.get('gewichtet_3', 'N/A')}%\n\n"
                        
                        return [types.TextContent(type="text", text=result)]
                    else:
                        return [types.TextContent(type="text", text=f"API request failed with status: {response.status}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error fetching data: {str(e)}")]
    
    elif name == "explain_variable":
        variable = arguments.get("variable", "")
        explanations = {
            "isin": "ISIN (International Securities Identification Number): A 12-character alphanumeric code that uniquely identifies a specific security. Format: 2-letter country code + 9-character national identifier + 1 check digit.",
            "date": "Date: The date when the cost of equity estimates were calculated, typically in YYYY-MM-DD format. Shows when the financial analysis was performed.",
            "MV": "MV (Market Value): The market capitalization of the company in millions of currency units. Calculated as stock price multiplied by number of outstanding shares.",
            "ddm_3": "DDM_3 (Dividend Discount Model 3-year): A cost of equity estimate based on the dividend discount model over a 3-year period. This model values a stock based on the present value of its expected future dividends.",
            "rim_3": "RIM_3 (Residual Income Model 3-year): A cost of equity estimate using the residual income model over 3 years. This model considers the company's ability to generate returns above its cost of capital.",
            "gewichtet_3": "Gewichtet_3 (Weighted 3-year): A weighted average cost of equity estimate combining the DDM and RIM models over 3 years. This provides a more balanced estimate by incorporating both valuation approaches."
        }
        
        explanation = explanations.get(variable, f"Variable '{variable}' not found in the API documentation.")
        return [types.TextContent(type="text", text=explanation)]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Main entry point for the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="marktrendite-api-info",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())

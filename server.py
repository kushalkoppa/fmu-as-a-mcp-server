"""
MCP Server for FMU Virtual ECU
This server exposes the Virtual ECU functionality as MCP tools
"""

import asyncio
import os
from typing import Any
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
import mcp.types as types
from fmu_model import VirtualECU

# Initialize the Virtual ECU
ecu = VirtualECU()

# Create MCP server
server = Server("fmu-virtual-ecu")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List all available tools for the Virtual ECU.
    """
    return [
        types.Tool(
            name="get_ecu_info",
            description="Get comprehensive information about the Virtual ECU including software version, interfaces, ECU level, and capabilities",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        types.Tool(
            name="get_software_version",
            description="Get the software version of the Virtual ECU",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        types.Tool(
            name="get_interfaces",
            description="Get the list of supported communication interfaces (CAN, LIN, Ethernet, FlexRay)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        types.Tool(
            name="get_ecu_level",
            description="Get the ECU level (e.g., Level_1, Level_2, etc.)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        types.Tool(
            name="perform_addition",
            description="Perform addition operation using the Virtual ECU. This demonstrates the computational capability of the FMU.",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number to add",
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number to add",
                    },
                },
                "required": ["a", "b"],
            },
        ),
        types.Tool(
            name="get_ecu_status",
            description="Get the current operational status of the Virtual ECU",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool calls for the Virtual ECU.
    """
    if name == "get_ecu_info":
        info = ecu.get_info()
        return [
            types.TextContent(
                type="text",
                text=f"""Virtual ECU Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Software: {info['software']}
Version: {info['version']}
ECU Level: {info['ecu_level']}
Manufacturer: {info['manufacturer']}
Build Date: {info['build_date']}

Supported Interfaces:
{chr(10).join(f'  • {interface}' for interface in info['interfaces'])}

Capabilities:
{chr(10).join(f'  • {cap}' for cap in info['capabilities'])}

Status: {info['status']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
            )
        ]
    
    elif name == "get_software_version":
        version = ecu.get_version()
        return [
            types.TextContent(
                type="text",
                text=f"Virtual ECU Software Version: {version}"
            )
        ]
    
    elif name == "get_interfaces":
        interfaces = ecu.get_interfaces()
        return [
            types.TextContent(
                type="text",
                text=f"Supported Communication Interfaces:\n" + 
                     "\n".join(f"  • {interface}" for interface in interfaces)
            )
        ]
    
    elif name == "get_ecu_level":
        level = ecu.get_ecu_level()
        return [
            types.TextContent(
                type="text",
                text=f"Virtual ECU Level: {level}"
            )
        ]
    
    elif name == "perform_addition":
        if not arguments:
            raise ValueError("Missing arguments for addition operation")
        
        a = arguments.get("a")
        b = arguments.get("b")
        
        if a is None or b is None:
            raise ValueError("Both 'a' and 'b' parameters are required")
        
        result = ecu.add(float(a), float(b))
        return [
            types.TextContent(
                type="text",
                text=f"Addition Result: {a} + {b} = {result}"
            )
        ]
    
    elif name == "get_ecu_status":
        status = ecu.get_status()
        return [
            types.TextContent(
                type="text",
                text=f"ECU Status: {status['status']}\nTimestamp: {status['timestamp']}"
            )
        ]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """
    Main entry point for the MCP server.
    """
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="fmu-virtual-ecu",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())

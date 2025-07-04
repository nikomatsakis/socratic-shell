"""MCP server implementation for dialectic pattern testing."""

from __future__ import annotations

import json
from typing import Any

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent, ServerCapabilities, ToolsCapability

from .models import PatternTest
from .sampling import SamplingEngine


class DialecticServer:
    """MCP server for testing collaboration patterns."""
    
    def __init__(self) -> None:
        """Initialize the dialectic server."""
        self.server: Server[Any, Any] = Server("dialectic", version="0.1.0")
        self._setup_tools()
    
    def _setup_tools(self) -> None:
        """Register MCP tools."""
        
        # MCP decorator typing: Decorator[[], Callable[[], Awaitable[list[Tool]]]]
        @self.server.list_tools()  # type: ignore[misc, no-untyped-call]
        async def handle_list_tools() -> list[Tool]:
            """List available tools for dialectic pattern testing."""
            return [
                Tool(
                    name="test_pattern",
                    description="Test a collaboration pattern with multiple scenarios",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "base_context": {
                                "type": "string",
                                "description": "Base conversation context to establish the scenario",
                            },
                            "system_prompt_path": {
                                "type": "string",
                                "description": "Path to file containing the system prompt",
                            },
                            "system_reminders_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Paths to files containing system reminders (e.g., CLAUDE.md)",
                                "default": [],
                            },
                            "test_scenarios": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Array of test statements/transitions to sample responses for",
                            },
                            "sampling_config": {
                                "type": "object",
                                "properties": {
                                    "temperature": {
                                        "type": "number",
                                        "minimum": 0.0,
                                        "maximum": 2.0,
                                        "default": 0.7,
                                    },
                                    "max_tokens": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "default": 500,
                                    },
                                    "include_reasoning": {
                                        "type": "boolean",
                                        "default": False,
                                    },
                                },
                                "additionalProperties": False,
                            },
                        },
                        "required": ["base_context", "test_scenarios"],
                        "additionalProperties": False,
                    },
                )
            ]
        
        # MCP decorator typing: Decorator[[], Callable[[str, dict[str, Any]], Awaitable[list[TextContent]]]]
        @self.server.call_tool()  # type: ignore[misc, no-untyped-call]
        async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
            """Handle tool calls."""
            if name == "test_pattern":
                return await self._handle_test_pattern(arguments)
            
            raise ValueError(f"Unknown tool: {name}")
    
    async def _handle_test_pattern(self, arguments: dict[str, Any]) -> list[TextContent]:
        """Handle test_pattern tool call."""
        # Parse and validate input
        pattern_test = PatternTest.model_validate(arguments)
        
        # For now, return a placeholder response indicating the server is working
        # TODO: Implement actual sampling when MCP sampling capabilities are available
        placeholder_results = {
            "pattern_test": pattern_test.model_dump(),
            "results": [
                {
                    "test_scenario": scenario,
                    "response": f"[PLACEHOLDER] This would be Claude's response to: {scenario}",
                    "metadata": {
                        "token_count": 50,
                        "response_time_ms": 100.0,
                        "sampling_config": pattern_test.sampling_config.model_dump(),
                    }
                }
                for scenario in pattern_test.test_scenarios
            ],
            "summary": {
                "total_scenarios": len(pattern_test.test_scenarios),
                "total_tokens": 50 * len(pattern_test.test_scenarios),
                "avg_response_time_ms": 100.0,
                "completed_at": 1703980800.0,
            }
        }
        
        # Return results as JSON
        return [
            TextContent(
                type="text",
                text=json.dumps(placeholder_results, indent=2),
            )
        ]
    
    
    async def run(self) -> None:
        """Run the MCP server."""
        from mcp import stdio_server
        
        options = InitializationOptions(
            server_name="dialectic",
            server_version="0.1.0",
            capabilities=ServerCapabilities(
                tools=ToolsCapability(listChanged=False)
            ),
        )
        
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream=read_stream,
                write_stream=write_stream,
                initialization_options=options,
            )
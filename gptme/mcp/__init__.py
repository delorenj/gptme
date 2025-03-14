"""
Model Context Protocol (MCP) client functionality.
"""

from .client import MCPClient, detect_mcp_config, load_mcp_config

__all__ = ["MCPClient", "detect_mcp_config", "load_mcp_config"]
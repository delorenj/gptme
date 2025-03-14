"""
Tests for the MCP TUI functionality.
"""

import json
import tempfile
from io import StringIO
from pathlib import Path

import pytest
from rich.console import Console

from gptme.mcp import MCPClient
from gptme.mcp.tui import display_mcp_info, display_sequential_thinking_status


def test_display_mcp_info_no_config():
    """Test display_mcp_info when no config is found."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a string buffer to capture output
        string_io = StringIO()
        console = Console(file=string_io, width=100)
        
        # Change to temp directory with no config
        with pytest.MonkeyPatch.context() as mp:
            mp.chdir(temp_dir)
            display_mcp_info(console=console)
        
        output = string_io.getvalue()
        assert "No MCP configuration detected" in output


def test_display_mcp_info_with_config():
    """Test display_mcp_info with a config file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        mcp_file = temp_path / "mcp.json"
        
        # Create test config
        config = {
            "version": "1.0",
            "sequential-thinking": {
                "enabled": True,
                "steps": 3,
                "description": "Test description"
            }
        }
        
        with open(mcp_file, "w") as f:
            json.dump(config, f)
        
        # Create a string buffer to capture output
        string_io = StringIO()
        console = Console(file=string_io, width=100)
        
        display_mcp_info(mcp_file, console=console)
        
        output = string_io.getvalue()
        assert "MCP Configuration" in output
        assert "Sequential Thinking" in output
        assert "Enabled" in output
        assert "steps" in output
        assert "3" in output


def test_display_sequential_thinking_status_enabled():
    """Test display_sequential_thinking_status with sequential thinking enabled."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        mcp_file = temp_path / "mcp.json"
        
        # Create test config with sequential thinking
        config = {
            "version": "1.0",
            "sequential-thinking": {
                "enabled": True,
                "steps": 5,
                "description": "Test sequential thinking"
            }
        }
        
        with open(mcp_file, "w") as f:
            json.dump(config, f)
        
        # Create a string buffer to capture output
        string_io = StringIO()
        console = Console(file=string_io, width=100)
        
        client = MCPClient(mcp_file)
        display_sequential_thinking_status(client, console=console)
        
        output = string_io.getvalue()
        assert "Sequential Thinking" in output
        assert "Enabled" in output
        assert "5" in output
        assert "Test sequential thinking" in output


def test_display_sequential_thinking_status_disabled():
    """Test display_sequential_thinking_status with sequential thinking disabled."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        mcp_file = temp_path / "mcp.json"
        
        # Create test config without sequential thinking
        config = {
            "version": "1.0"
        }
        
        with open(mcp_file, "w") as f:
            json.dump(config, f)
        
        # Create a string buffer to capture output
        string_io = StringIO()
        console = Console(file=string_io, width=100)
        
        client = MCPClient(mcp_file)
        display_sequential_thinking_status(client, console=console)
        
        output = string_io.getvalue()
        assert "Sequential Thinking Status" in output
        assert "not enabled" in output
"""
Tests for the MCP client functionality.
"""

import json
import os
import tempfile
from pathlib import Path

import pytest

from gptme.mcp import MCPClient, detect_mcp_config, load_mcp_config


def test_detect_mcp_config_not_found():
    """Test that detect_mcp_config returns None when no config is found."""
    with tempfile.TemporaryDirectory() as temp_dir:
        assert detect_mcp_config(temp_dir) is None


def test_detect_mcp_config_found():
    """Test that detect_mcp_config returns the path when config is found."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        mcp_file = temp_path / "mcp.json"
        
        with open(mcp_file, "w") as f:
            json.dump({"version": "1.0"}, f)
        
        detected = detect_mcp_config(temp_dir)
        assert detected is not None
        assert detected.name == "mcp.json"
        # On macOS, the temporary directory path might be resolved differently
        # So we just check that the file exists and has the right name


def test_load_mcp_config():
    """Test loading MCP configuration from file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        mcp_file = temp_path / "mcp.json"
        
        expected_config = {
            "version": "1.0",
            "sequential-thinking": {
                "enabled": True,
                "steps": 3
            }
        }
        
        with open(mcp_file, "w") as f:
            json.dump(expected_config, f)
        
        config = load_mcp_config(mcp_file)
        assert config == expected_config


def test_load_mcp_config_file_not_found():
    """Test that load_mcp_config raises FileNotFoundError when file doesn't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        non_existent_file = Path(temp_dir) / "non_existent.json"
        
        with pytest.raises(FileNotFoundError):
            load_mcp_config(non_existent_file)


def test_load_mcp_config_invalid_json():
    """Test that load_mcp_config raises ValueError for invalid JSON."""
    with tempfile.TemporaryDirectory() as temp_dir:
        invalid_file = Path(temp_dir) / "invalid.json"
        
        with open(invalid_file, "w") as f:
            f.write("This is not valid JSON")
        
        with pytest.raises(ValueError):
            load_mcp_config(invalid_file)


def test_mcp_client_init_with_path():
    """Test initializing MCPClient with a specific config path."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        mcp_file = temp_path / "mcp.json"
        
        config = {
            "version": "1.0",
            "sequential-thinking": {
                "enabled": True
            }
        }
        
        with open(mcp_file, "w") as f:
            json.dump(config, f)
        
        client = MCPClient(mcp_file)
        assert client.config_path == mcp_file
        assert client.config == config
        assert client.has_sequential_thinking is True


def test_mcp_client_auto_detect():
    """Test that MCPClient auto-detects config when no path is provided."""
    original_dir = os.getcwd()
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            mcp_file = temp_path / "mcp.json"
            
            config = {"version": "1.0"}
            
            with open(mcp_file, "w") as f:
                json.dump(config, f)
            
            os.chdir(temp_dir)
            client = MCPClient()
            assert client.config_path is not None
            assert client.config == config
    finally:
        os.chdir(original_dir)


def test_mcp_client_sequential_thinking():
    """Test the has_sequential_thinking property."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create config with sequential thinking
        mcp_file_with = temp_path / "with_st.json"
        config_with = {
            "version": "1.0",
            "sequential-thinking": {
                "enabled": True
            }
        }
        with open(mcp_file_with, "w") as f:
            json.dump(config_with, f)
        
        # Create config without sequential thinking
        mcp_file_without = temp_path / "without_st.json"
        config_without = {"version": "1.0"}
        with open(mcp_file_without, "w") as f:
            json.dump(config_without, f)
        
        # Test with sequential thinking
        client_with = MCPClient(mcp_file_with)
        assert client_with.has_sequential_thinking is True
        
        # Test without sequential thinking
        client_without = MCPClient(mcp_file_without)
        assert client_without.has_sequential_thinking is False
        
        # Test with no config
        client_none = MCPClient(None)
        assert client_none.has_sequential_thinking is False
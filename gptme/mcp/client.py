"""
Model Context Protocol (MCP) client functionality.

This module provides functionality for detecting, loading, and interacting with
MCP configuration files.
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Union

logger = logging.getLogger(__name__)


def detect_mcp_config(directory: Union[str, Path] = ".") -> Optional[Path]:
    """
    Detect MCP configuration file in the given directory.

    Args:
        directory: Directory to search for MCP configuration file. Defaults to current directory.

    Returns:
        Path to the MCP configuration file if found, None otherwise.
    """
    directory = Path(directory).resolve()
    mcp_file = directory / "mcp.json"
    
    if mcp_file.exists():
        logger.info(f"MCP configuration detected: {mcp_file}")
        return mcp_file
    
    return None


def load_mcp_config(file_path: Union[str, Path]) -> Dict:
    """
    Load MCP configuration from file.

    Args:
        file_path: Path to the MCP configuration file.

    Returns:
        Dictionary containing the MCP configuration.
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"MCP configuration file not found: {file_path}")
    
    try:
        with open(file_path, "r") as f:
            config = json.load(f)
        
        logger.info(f"Loaded MCP configuration from {file_path}")
        
        # Validate if it has sequential-thinking configured
        if "sequential-thinking" in config:
            logger.info("Sequential thinking configuration detected")
        
        return config
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing MCP configuration: {e}")
        raise ValueError(f"Invalid MCP configuration file: {e}")


class MCPClient:
    """
    Client for interacting with MCP servers.
    """
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """
        Initialize the MCP client.

        Args:
            config_path: Path to the MCP configuration file. If None, attempts to detect it.
        """
        self.config_path = None
        self.config = None
        
        if config_path:
            self.config_path = Path(config_path)
            self.config = load_mcp_config(self.config_path)
        else:
            detected_path = detect_mcp_config()
            if detected_path:
                self.config_path = detected_path
                self.config = load_mcp_config(self.config_path)
    
    @property
    def has_sequential_thinking(self) -> bool:
        """Check if sequential thinking is configured."""
        if not self.config:
            return False
        return "sequential-thinking" in self.config
    
    def get_config(self) -> Optional[Dict]:
        """Get the loaded MCP configuration."""
        return self.config
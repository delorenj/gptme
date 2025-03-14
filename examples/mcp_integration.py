"""
Example demonstrating how to use the MCP client functionality.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to sys.path to import gptme
sys.path.insert(0, str(Path(__file__).parent.parent))

from gptme.mcp import MCPClient, detect_mcp_config, load_mcp_config
from gptme.util import console


def main():
    """Main function demonstrating MCP client usage."""
    # Get the directory where this script is located
    examples_dir = Path(__file__).parent
    
    # Check for MCP configuration
    mcp_config_path = detect_mcp_config(examples_dir)
    
    if mcp_config_path:
        console.log(f"[bold green]MCP configuration detected:[/bold green] {mcp_config_path}")
        
        try:
            # Load the configuration
            mcp_config = load_mcp_config(mcp_config_path)
            console.log(f"Configuration loaded: {mcp_config}")
            
            # Create an MCP client
            client = MCPClient(mcp_config_path)
            
            # Check for sequential thinking
            if client.has_sequential_thinking:
                console.log("[bold green]Sequential thinking is enabled![/bold green]")
            else:
                console.log("Sequential thinking is not enabled.")
                
        except Exception as e:
            console.log(f"[bold red]Error loading MCP configuration:[/bold red] {e}")
    else:
        console.log("[bold yellow]No MCP configuration detected.[/bold yellow]")


if __name__ == "__main__":
    main()
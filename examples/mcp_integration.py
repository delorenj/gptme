"""
Example demonstrating how to use the MCP client functionality with fancy TUI.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to sys.path to import gptme
sys.path.insert(0, str(Path(__file__).parent.parent))

from gptme.mcp import (
    MCPClient, 
    detect_mcp_config, 
    load_mcp_config,
    display_mcp_info,
    display_sequential_thinking_status
)
from gptme.util import console
from rich.console import Console
from rich.panel import Panel


def main():
    """Main function demonstrating MCP client usage with fancy TUI."""
    # Get the directory where this script is located
    examples_dir = Path(__file__).parent
    
    console = Console()
    console.print(Panel(
        "[bold blue]MCP Client Demo[/bold blue]\n\n"
        "This example demonstrates the MCP client functionality with a fancy TUI.\n"
        "It will detect and display MCP configuration in the current directory.",
        title="MCP Integration Example",
        border_style="cyan"
    ))
    
    console.print()
    
    # Check for MCP configuration
    mcp_config_path = detect_mcp_config(examples_dir)
    
    if mcp_config_path:
        try:
            # Display MCP configuration with fancy TUI
            display_mcp_info(mcp_config_path, console=console)
            
            # Create an MCP client
            client = MCPClient(mcp_config_path)
            
            # Display sequential thinking status
            console.print()
            display_sequential_thinking_status(client, console=console)
                
        except Exception as e:
            console.print(Panel(
                f"[bold red]Error:[/bold red] {e}",
                title="Error",
                border_style="red"
            ))
    else:
        console.print(Panel(
            "[yellow]No MCP configuration detected in this directory.[/yellow]\n\n"
            "To test this example, create an mcp.json file with sequential-thinking configured.",
            title="No Configuration Found",
            border_style="yellow"
        ))


if __name__ == "__main__":
    main()
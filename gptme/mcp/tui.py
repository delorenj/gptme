"""
Text User Interface components for displaying MCP information.
"""

import json
from pathlib import Path
from typing import Dict, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

from .client import MCPClient, detect_mcp_config, load_mcp_config


def display_mcp_info(config_path: Optional[Path] = None, console: Optional[Console] = None) -> None:
    """
    Display MCP configuration information in a fancy TUI.

    Args:
        config_path: Path to MCP configuration file. If None, attempts to detect it.
        console: Rich console to use for display. If None, creates a new one.
    """
    if console is None:
        console = Console()

    # Detect MCP config if not provided
    if config_path is None:
        config_path = detect_mcp_config()
        if config_path is None:
            console.print(Panel("[yellow]No MCP configuration detected[/yellow]", 
                               title="MCP Status",
                               border_style="yellow"))
            return

    try:
        # Load configuration
        config = load_mcp_config(config_path)
        client = MCPClient(config_path)

        # Create main panel
        tree = Tree(f"[bold blue]MCP Configuration:[/bold blue] {config_path}")
        
        # Add version info
        if "version" in config:
            tree.add(f"[cyan]Version:[/cyan] {config['version']}")
        
        # Add sequential thinking info
        if client.has_sequential_thinking:
            st_node = tree.add("[bold green]Sequential Thinking:[/bold green] Enabled")
            st_config = config.get("sequential-thinking", {})
            
            for key, value in st_config.items():
                if key != "enabled":
                    st_node.add(f"[green]{key}:[/green] {value}")
        
        # Add tools info if present
        if "tools" in config:
            tools_node = tree.add(f"[bold magenta]Tools:[/bold magenta] {len(config['tools'])} defined")
            for tool in config.get("tools", []):
                tool_name = tool.get("name", "Unnamed tool")
                tool_desc = tool.get("description", "No description")
                tools_node.add(f"[magenta]{tool_name}:[/magenta] {tool_desc}")
        
        # Add resources info if present
        if "resources" in config:
            resources_node = tree.add(f"[bold yellow]Resources:[/bold yellow] {len(config['resources'])} defined")
            for resource in config.get("resources", []):
                resource_id = resource.get("id", "Unknown ID")
                resource_type = resource.get("type", "Unknown type")
                resources_node.add(f"[yellow]{resource_id}:[/yellow] {resource_type}")
        
        # Add prompts info if present
        if "prompts" in config:
            prompts_node = tree.add(f"[bold cyan]Prompts:[/bold cyan] {len(config['prompts'])} defined")
            for prompt in config.get("prompts", []):
                prompt_id = prompt.get("id", "Unknown ID")
                prompt_title = prompt.get("title", "Untitled")
                prompts_node.add(f"[cyan]{prompt_id}:[/cyan] {prompt_title}")
        
        # Display the tree in a panel
        console.print(Panel(tree, title="MCP Configuration", border_style="green"))
        
    except Exception as e:
        console.print(Panel(f"[bold red]Error loading MCP configuration:[/bold red] {str(e)}", 
                           title="MCP Error",
                           border_style="red"))


def display_sequential_thinking_status(client: Optional[MCPClient] = None, 
                                      console: Optional[Console] = None) -> None:
    """
    Display a focused panel showing sequential thinking status.
    
    Args:
        client: MCPClient instance. If None, creates a new one.
        console: Rich console to use for display. If None, creates a new one.
    """
    if console is None:
        console = Console()
        
    if client is None:
        config_path = detect_mcp_config()
        if config_path:
            client = MCPClient(config_path)
        else:
            console.print(Panel("[yellow]No MCP configuration detected[/yellow]", 
                               title="Sequential Thinking Status",
                               border_style="yellow"))
            return
    
    if client.has_sequential_thinking:
        st_config = client.config.get("sequential-thinking", {})
        steps = st_config.get("steps", "Not specified")
        description = st_config.get("description", "No description provided")
        
        table = Table(show_header=False, box=None)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Status", "[bold green]Enabled[/bold green]")
        table.add_row("Steps", str(steps))
        table.add_row("Description", description)
        
        console.print(Panel(table, title="Sequential Thinking", border_style="green"))
    else:
        console.print(Panel("[yellow]Sequential Thinking is not enabled[/yellow]", 
                           title="Sequential Thinking Status",
                           border_style="yellow"))


if __name__ == "__main__":
    # Example usage
    console = Console()
    display_mcp_info(console=console)
    console.print()
    display_sequential_thinking_status(console=console)
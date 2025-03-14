Model Context Protocol (MCP)
=========================

This document describes the integration of the `Model Context Protocol (MCP) <https://modelcontextprotocol.io/>`_ in gptme.

.. contents::
   :local:

Overview
--------

The Model Context Protocol (MCP) is an open standard for AI models, clients, and tools to communicate with each other. 
gptme implements MCP client functionality, allowing it to detect and utilize MCP configuration files in workspaces.

Currently, gptme supports detection and notification of MCP configurations, with specific support for sequential-thinking functionality.

Installation
-----------

MCP functionality is included in the standard gptme installation. No additional installation steps are required.

Usage
-----

Basic Usage
~~~~~~~~~~

When you run gptme in a directory containing an ``mcp.json`` file, it will automatically detect and display information about the MCP configuration:

.. code-block:: bash

   cd /path/with/mcp.json
   gptme "Your prompt here"

The MCP configuration will be displayed in a fancy TUI (Text User Interface) at startup.

Creating an MCP Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use MCP with gptme, create an ``mcp.json`` file in your workspace directory:

.. code-block:: json

   {
     "version": "1.0",
     "sequential-thinking": {
       "enabled": true,
       "steps": 3,
       "description": "Break down complex problems into steps"
     }
   }

This configuration enables sequential-thinking with 3 steps.

Features
--------

Sequential Thinking
~~~~~~~~~~~~~~~~~~

Sequential thinking allows models to break down complex problems into a series of steps. When enabled in an MCP configuration, gptme will display this capability.

Configuration options for sequential-thinking:

- ``enabled``: Boolean indicating if sequential-thinking is enabled
- ``steps``: Number of steps to use (optional)
- ``description``: Description of the sequential-thinking process (optional)

Future MCP Features
~~~~~~~~~~~~~~~~~~

The following MCP features are planned for future implementation:

- Tools support
- Resources support
- Prompts support
- Full MCP server connectivity

Developer API
------------

Client API
~~~~~~~~~

The MCP client API is available in the ``gptme.mcp`` module:

.. code-block:: python

   from gptme.mcp import MCPClient, detect_mcp_config, load_mcp_config

   # Detect MCP configuration
   config_path = detect_mcp_config()
   
   # Load configuration
   if config_path:
       config = load_mcp_config(config_path)
       
   # Create client
   client = MCPClient(config_path)
   
   # Check for sequential thinking
   if client.has_sequential_thinking:
       print("Sequential thinking is enabled")

TUI API
~~~~~~~

The MCP module includes a TUI (Text User Interface) for displaying MCP information:

.. code-block:: python

   from gptme.mcp import display_mcp_info, display_sequential_thinking_status
   
   # Display comprehensive MCP info
   display_mcp_info()
   
   # Display focused sequential thinking status
   display_sequential_thinking_status()

Programmatic Usage
~~~~~~~~~~~~~~~~~

You can integrate MCP functionality into your own code:

.. code-block:: python

   import os
   from pathlib import Path
   from gptme.mcp import MCPClient, detect_mcp_config

   # Change to a specific directory
   os.chdir('/path/to/workspace')
   
   # Detect MCP configuration
   config_path = detect_mcp_config()
   
   if config_path:
       # Create client
       client = MCPClient(config_path)
       
       # Access configuration
       config = client.config
       
       # Check for sequential thinking
       if client.has_sequential_thinking:
           st_config = config.get('sequential-thinking', {})
           steps = st_config.get('steps', 3)
           print(f"Sequential thinking enabled with {steps} steps")

Testing
-------

The MCP implementation includes comprehensive tests:

- ``tests/test_mcp_client.py``: Tests for the client functionality
- ``tests/test_mcp_tui.py``: Tests for the TUI components

Run the tests with:

.. code-block:: bash

   python -m pytest tests/test_mcp_client.py tests/test_mcp_tui.py -v

Examples
--------

Example Configuration
~~~~~~~~~~~~~~~~~~~~

A basic ``mcp.json`` file with sequential-thinking:

.. code-block:: json

   {
     "version": "1.0",
     "sequential-thinking": {
       "enabled": true,
       "steps": 3,
       "description": "Break down complex problems into steps"
     }
   }

Example Usage
~~~~~~~~~~~~

An example script demonstrating MCP functionality is available at ``examples/mcp_integration.py``:

.. code-block:: bash

   python examples/mcp_integration.py

References
---------

- `Model Context Protocol <https://modelcontextprotocol.io/>`_
- `MCP Client Documentation <https://modelcontextprotocol.io/quickstart/client>`_
- `Sequential Thinking <https://modelcontextprotocol.io/docs/concepts/sequential-thinking>`_
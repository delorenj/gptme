#!/usr/bin/env python3
"""
Tool for analyzing gptme tools and their dependencies.
Helps developers understand the codebase and identify areas for improvement.
"""

import os
import sys
import ast
import importlib
from pathlib import Path
from typing import Dict, List, Set

def find_tool_files(gptme_path: Path) -> List[Path]:
    """Find all tool implementation files in the gptme codebase."""
    tools_dir = gptme_path / "gptme" / "tools"
    return list(tools_dir.glob("*.py"))

def analyze_tool_file(file_path: Path) -> Dict:
    """Analyze a tool implementation file for dependencies and structure."""
    with open(file_path) as f:
        content = f.read()
    
    tree = ast.parse(content)
    
    # Extract basic information
    info = {
        "name": file_path.stem,
        "imports": set(),
        "classes": [],
        "functions": [],
        "tool_specs": []
    }
    
    # Analyze the AST
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                info["imports"].add(name.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                info["imports"].add(node.module)
        elif isinstance(node, ast.ClassDef):
            info["classes"].append(node.name)
        elif isinstance(node, ast.FunctionDef):
            info["functions"].append(node.name)
        # Look for ToolSpec assignments
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if any(isinstance(node.value, ast.Call) and 
                          isinstance(node.value.func, ast.Name) and 
                          node.value.func.id == "ToolSpec"):
                        info["tool_specs"].append(target.id)
    
    return info

def main():
    # Find gptme root directory (parent of current directory)
    gptme_path = Path(__file__).parent.parent
    
    print(f"Analyzing gptme tools in: {gptme_path}")
    print("-" * 80)
    
    tool_files = find_tool_files(gptme_path)
    
    for tool_file in sorted(tool_files):
        if tool_file.name.startswith('_'):
            continue
            
        print(f"\nAnalyzing {tool_file.name}:")
        try:
            info = analyze_tool_file(tool_file)
            
            if info["tool_specs"]:
                print(f"  Tool Specs: {', '.join(info['tool_specs'])}")
            
            print("  Functions:", ', '.join(info["functions"]) or "None")
            
            # Show relevant imports (exclude standard library)
            relevant_imports = {imp for imp in info["imports"] 
                              if 'gptme' in imp or '.' in imp}
            if relevant_imports:
                print("  Dependencies:", ', '.join(sorted(relevant_imports)))
            
        except Exception as e:
            print(f"  Error analyzing {tool_file}: {e}")
    
    print("\nSummary:")
    print(f"Found {len(tool_files)} tool files")

if __name__ == "__main__":
    main()

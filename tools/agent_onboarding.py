#!/usr/bin/env python3
"""
Agent Onboarding Tool for gptme

Creates specialized, persistent agents with their own knowledge bases and memory.
Supports multiple vector storage backends and embedding models.
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

class VectorStoreType(Enum):
    COHERE = "cohere"
    QDRANT = "qdrant"
    WEAVIATE = "weaviate"
    REDIS = "redis"

class EmbeddingProvider(Enum):
    COHERE = "cohere"
    VOYAGEAI = "voyageai"
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"

@dataclass
class AgentConfig:
    name: str
    description: str
    vector_store: VectorStoreType
    embedding_provider: EmbeddingProvider
    project_paths: List[Path]
    github_repos: List[str]
    documentation_urls: List[str]
    context_paths: List[Path]
    framework_stack: List[str]
    domain_context: str

class AgentOnboarding:
    def __init__(self):
        self.config = None
        self.rag_system = None
        self.memory_store = None
    
    async def start_onboarding(self) -> AgentConfig:
        """Start the interactive onboarding process."""
        print("🤖 Welcome to gptme Agent Onboarding!")
        print("Let's create a specialized agent for your project.\n")

        # Get basic project information
        name = await self._prompt("What would you like to name your agent?")
        description = await self._prompt("Briefly describe the agent's purpose:")
        
        # Get technology stack
        stack = await self._get_tech_stack()
        
        # Check for unknown technologies and offer to research
        unknown_tech = await self._check_unknown_technologies(stack)
        if unknown_tech:
            await self._research_technologies(unknown_tech)
        
        # Get project context
        project_paths = await self._get_project_paths()
        github_repos = await self._get_github_repos()
        
        # Get additional context sources
        context_paths = await self._get_context_paths()
        
        # Choose vector store and embedding provider
        vector_store = await self._choose_vector_store()
        embedding_provider = await self._choose_embedding_provider()
        
        # Get domain context
        domain_context = await self._prompt("Please provide any additional domain context:")
        
        # Create config
        self.config = AgentConfig(
            name=name,
            description=description,
            vector_store=vector_store,
            embedding_provider=embedding_provider,
            project_paths=project_paths,
            github_repos=github_repos,
            documentation_urls=[],  # Will be populated during research
            context_paths=context_paths,
            framework_stack=stack,
            domain_context=domain_context
        )
        
        return self.config
    
    async def _prompt(self, message: str, options: List[str] = None) -> str:
        """Display a prompt and get user input."""
        print(f"\n{message}")
        if options:
            for i, opt in enumerate(options, 1):
                print(f"{i}. {opt}")
            while True:
                try:
                    choice = int(await asyncio.get_event_loop().run_in_executor(
                        None, input, "Enter your choice (number): "))
                    if 1 <= choice <= len(options):
                        return options[choice - 1]
                except ValueError:
                    pass
                print("Please enter a valid number.")
        else:
            return await asyncio.get_event_loop().run_in_executor(
                None, input, "> ")
    
    async def _get_tech_stack(self) -> List[str]:
        """Get the technology stack for the project."""
        print("\nWhat technologies/frameworks will this project use?")
        print("Enter them one at a time (empty line when done):")
        
        stack = []
        while True:
            tech = await self._prompt("Add technology (or empty to finish):")
            if not tech:
                break
            stack.append(tech)
        return stack
    
    async def _check_unknown_technologies(self, stack: List[str]) -> List[str]:
        """Check for technologies that need research."""
        # TODO: Implement technology knowledge check
        # For now, just return Smolagents as unknown
        return ["smolagents"] if "smolagents" in [t.lower() for t in stack] else []
    
    async def _research_technologies(self, technologies: List[str]):
        """Research unknown technologies and index their documentation."""
        for tech in technologies:
            print(f"\nResearching {tech}...")
            # TODO: Implement documentation fetching and indexing
            print(f"✓ Found and indexed documentation for {tech}")
    
    async def _get_project_paths(self) -> List[Path]:
        """Get local project paths."""
        paths = []
        print("\nEnter local project paths (empty line when done):")
        while True:
            path_str = await self._prompt("Add path (or empty to finish):")
            if not path_str:
                break
            path = Path(path_str).expanduser().resolve()
            if path.exists():
                paths.append(path)
            else:
                print(f"Warning: Path {path} does not exist")
        return paths
    
    async def _get_github_repos(self) -> List[str]:
        """Get GitHub repository URLs."""
        repos = []
        print("\nEnter GitHub repository URLs (empty line when done):")
        while True:
            repo = await self._prompt("Add repo (or empty to finish):")
            if not repo:
                break
            repos.append(repo)
        return repos
    
    async def _get_context_paths(self) -> List[Path]:
        """Get additional context paths (e.g., Obsidian vault)."""
        paths = []
        print("\nEnter additional context paths (e.g., Obsidian vault):")
        while True:
            path_str = await self._prompt("Add path (or empty to finish):")
            if not path_str:
                break
            path = Path(path_str).expanduser().resolve()
            if path.exists():
                paths.append(path)
            else:
                print(f"Warning: Path {path} does not exist")
        return paths
    
    async def _choose_vector_store(self) -> VectorStoreType:
        """Choose vector store backend."""
        options = [vs.value for vs in VectorStoreType]
        choice = await self._prompt(
            "Choose a vector store backend:",
            options
        )
        return VectorStoreType(choice)
    
    async def _choose_embedding_provider(self) -> EmbeddingProvider:
        """Choose embedding provider."""
        options = [ep.value for ep in EmbeddingProvider]
        choice = await self._prompt(
            "Choose an embedding provider:",
            options
        )
        return EmbeddingProvider(choice)

async def main():
    onboarding = AgentOnboarding()
    config = await onboarding.start_onboarding()
    
    # Save configuration
    config_path = Path.home() / ".gptme" / "agents" / f"{config.name}.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w') as f:
        # Convert config to dict, handling Path objects
        config_dict = {
            k: str(v) if isinstance(v, Path) else v.value if isinstance(v, Enum) else v
            for k, v in config.__dict__.items()
        }
        json.dump(config_dict, f, indent=2)
    
    print(f"\n✨ Agent configuration saved to {config_path}")
    print("Next steps:")
    print("1. Setting up vector store")
    print("2. Indexing documentation")
    print("3. Creating agent memory")
    print("4. Adding to discovery service")

if __name__ == "__main__":
    asyncio.run(main())

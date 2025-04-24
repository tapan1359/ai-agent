"""Tool factory for creating and managing cloud tools."""
from typing import List, Dict, Type

from langchain_core.tools import Tool

from .base import CloudTool
from .aws_cli import AWSCliTool


class CloudToolFactory:
    """Factory for creating and managing cloud tools."""

    def __init__(self):
        """Initialize the tool factory with available tools."""
        self._tools: Dict[str, Type[CloudTool]] = {
            "aws": AWSCliTool,
        }
        self._instances: Dict[str, CloudTool] = {}

    def get_tool(self, provider: str) -> Tool:
        """Get a tool for a specific provider.

        Args:
            provider (str): The cloud provider name (e.g., 'aws', 'azure', 'gcp')

        Returns:
            Tool: The configured tool for the provider
        """
        if provider not in self._instances:
            if provider not in self._tools:
                raise ValueError(f"Provider {provider} not supported")
            self._instances[provider] = self._tools[provider]()

        tool = self._instances[provider]
        return Tool(
            name=tool.name,
            description=tool.description,
            func=tool.run,
            coroutine=tool.arun
        )

    def get_all_tools(self) -> List[Tool]:
        """Get all available cloud tools.

        Returns:
            List[Tool]: List of all configured tools
        """
        return [self.get_tool(provider) for provider in self._tools.keys()]

    def find_tools_for_query(self, query: str) -> List[Tool]:
        """Find relevant tools based on the query.

        Args:
            query (str): The user's query

        Returns:
            List[Tool]: List of relevant tools for the query
        """
        query = query.lower()
        relevant_tools = []

        for provider in self._tools:
            tool = self.get_tool(provider)
            instance = self._instances[provider]
            
            # Check if any keywords match
            if any(keyword in query for keyword in instance.keywords):
                relevant_tools.append(tool)
                continue

            # Check if provider name is mentioned
            if provider in query:
                relevant_tools.append(tool)
                continue

            # Check if any capabilities are mentioned
            if any(cap in query for cap in instance.capabilities):
                relevant_tools.append(tool)

        # If no specific tools found, return all tools
        return relevant_tools if relevant_tools else self.get_all_tools()

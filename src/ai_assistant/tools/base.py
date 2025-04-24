"""Base classes for cloud tools."""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any

class CloudTool(ABC):
    """Base class for all cloud provider tools."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description."""
        pass
    
    @property
    @abstractmethod
    def provider(self) -> str:
        """Cloud provider name (e.g., 'aws', 'azure', 'gcp')."""
        pass

    @abstractmethod
    async def arun(self, command: str) -> str:
        """Run command asynchronously."""
        pass

    @abstractmethod
    def run(self, command: str) -> str:
        """Run command synchronously."""
        pass

    @property
    def capabilities(self) -> List[str]:
        """List of tool capabilities (e.g., ['storage', 'compute', 'network'])."""
        return []

    @property
    def keywords(self) -> List[str]:
        """Keywords that indicate this tool should be used."""
        return []

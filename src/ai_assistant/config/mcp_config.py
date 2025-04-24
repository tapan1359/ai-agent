"""Configuration for MCP servers."""
from typing import Dict, Any

MCP_SERVERS = {
    "awslabs.core-mcp-server": {
        "command": "uvx",
        "args": ["awslabs.core-mcp-server@latest"],
        "env": {"FASTMCP_LOG_LEVEL": "ERROR"}
    },
    "awslabs.aws-diagram-mcp-server": {
        "command": "uvx",
        "args": ["awslabs.aws-diagram-mcp-server@latest"],
        "env": {"FASTMCP_LOG_LEVEL": "ERROR"}
    },
    "awslabs.aws-documentation-mcp-server": {
        "command": "uvx",
        "args": ["awslabs.aws-documentation-mcp-server@latest"],
        "env": {"FASTMCP_LOG_LEVEL": "ERROR"}
    }
}

def get_mcp_config() -> Dict[str, Any]:
    """Get MCP server configuration.

    Returns:
        Dict[str, Any]: MCP server configuration dictionary
    """
    return MCP_SERVERS

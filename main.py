from langchain_aws import ChatBedrock
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

model = ChatBedrock(model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0")

async def main():
    async with MultiServerMCPClient(
        {
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
            },
            "Azure MCP Server": {
                "command": "npx",
                "args": [
                    "-y",
                    "@azure/mcp@latest",
                    "server",
                    "start"
                ],
            }
        }
    ) as client:
        agent = create_react_agent(model, client.get_tools())
        print("Welcome to the AI Agent Chat! Type 'exit' to quit.\n")
        while True:
            user_input = input("You: ")
            if user_input.lower() in {"exit", "quit"}:
                print("Exiting chat. Goodbye!")
                break
            async for step in agent.astream(
                {"messages": [HumanMessage(content=user_input)]},
                stream_mode="values",
            ):
                step["messages"][-1].pretty_print()

if __name__ == "__main__":
    asyncio.run(main())

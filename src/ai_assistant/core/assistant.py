"""Cloud Assistant using LangChain."""
import asyncio
from typing import Optional
from langchain_core.messages import HumanMessage
from langchain_aws import ChatBedrock
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from ..config.mcp_config import get_mcp_config
from ..tools.factory import CloudToolFactory

class CloudAssistant:
    """Assistant for interacting with cloud services."""

    def __init__(
        self,
        model_id: str = "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    ) -> None:
        """Initialize the Cloud Assistant.

        Args:
            model_id (str): Bedrock model ID to use
        """
        self.model = ChatBedrock(model_id=model_id)
        self.mcp_config = get_mcp_config()
        self.tool_factory = CloudToolFactory()
        self._print_welcome = True
        self.agent = None
        self.mcp_client = None

    def _print_welcome_message(self):
        """Print the welcome message with example questions."""
        print("\nWelcome to Cloud Assistant! Here are some example questions:")
        print("- List my EC2 instances")
        print("- Show my IAM users")
        print("- [Future] List my Azure VMs")

    async def _setup_agent(self) -> None:
        """Set up the agent with tools."""
        if self._print_welcome:
            self._print_welcome_message()
        
        if not self.mcp_client:
            self.mcp_client = MultiServerMCPClient(self.mcp_config)
            await self.mcp_client.__aenter__() 

        # Get MCP tools and combine with cloud tools
        mcp_tools = self.mcp_client.get_tools()
        all_tools = self.tool_factory.get_all_tools() + mcp_tools
            
        # Create agent with combined tools
        self.agent = create_react_agent(self.model, tools=all_tools)

    async def process_input(self, user_input: str) -> str:
        """Process a single user input and return the response."""
        if not hasattr(self, "agent"):
            await self._setup_agent()

        response = ""
        async for step in self.agent.astream(
            {"messages": [HumanMessage(content=user_input)]},
            stream_mode="values",
        ):
            response = step["messages"][-1].content
        return response

    async def _interaction_loop(self) -> None:
        """Run the main interaction loop."""
        await self._setup_agent()  # Initialize with all tools for CLI mode
        while True:
            user_input = input("You: ")
            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            response = await self.process_input(user_input)
            print(f"Assistant: {response}")

    async def start(self) -> None:
        """Start the Cloud Assistant in CLI mode."""
        await self._interaction_loop()

    async def cleanup(self) -> None:
        """Clean up resources."""
        if self.mcp_client:
            await self.mcp_client.__aexit__()

def get_assistant():
    """Get a configured Cloud Assistant instance."""
    assistant = CloudAssistant()
    return assistant

def run_assistant():
    """Run the Cloud Assistant in CLI mode."""
    assistant = get_assistant()
    asyncio.run(assistant.start())

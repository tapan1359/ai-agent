"""Core Cloud Assistant implementation."""
import asyncio
from typing import List, Optional

from langchain_aws import ChatBedrock
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import Tool
from langchain_mcp_adapters.client import MultiServerMCPClient

from ..config.mcp_config import get_mcp_config
from ..tools.factory import CloudToolFactory


class CloudAssistant:
    """Cloud Assistant that combines multiple cloud providers with documentation tools."""

    def __init__(self, model_id: str = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"):
        """Initialize the Cloud Assistant.

        Args:
            model_id (str): The model ID to use for the chat
        """
        self.model = ChatBedrock(model_id=model_id)
        self.mcp_config = get_mcp_config()
        self.tool_factory = CloudToolFactory()
        self._print_welcome = True

    def _print_welcome_message(self):
        """Print the welcome message with example questions."""
        print("Welcome to the Cloud Assistant! Type 'exit' to quit.\n")
        print("You can ask questions like:")
        print("- How many S3 buckets do I have?")
        print("- List my EC2 instances")
        print("- Show my IAM users")
        print("- [Future] List my Azure VMs")
        print("- [Future] Show my GCP storage buckets\n")

    async def _setup_agent(self) -> None:
        """Set up the agent with tools."""
        if self._print_welcome:
            self._print_welcome_message()
        
        # Load all tools at initialization
        all_tools = self.tool_factory.get_all_tools()
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
                print("Exiting chat. Goodbye!")
                break

            response = await self.process_input(user_input)
            print(f"Assistant: {response}")

    async def start(self) -> None:
        """Start the Cloud Assistant in CLI mode."""
        await self._interaction_loop()


def get_assistant():
    """Get a configured Cloud Assistant instance."""
    assistant = CloudAssistant()
    return assistant

def run_assistant():
    """Run the Cloud Assistant in CLI mode."""
    assistant = get_assistant()
    asyncio.run(assistant.start())

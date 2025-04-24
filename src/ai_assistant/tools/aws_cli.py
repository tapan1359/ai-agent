"""AWS CLI Tool for executing AWS commands."""
import asyncio
import shlex
import subprocess
from typing import List

from langchain_core.tools import Tool

from .base import CloudTool


class AWSCliTool(CloudTool):
    """A tool for executing AWS CLI commands."""

    @property
    def name(self) -> str:
        return "aws_cli"

    @property
    def description(self) -> str:
        return "Execute AWS CLI commands to interact with AWS services"

    @property
    def provider(self) -> str:
        return "aws"

    @property
    def capabilities(self) -> List[str]:
        return ["storage", "compute", "network", "identity", "database"]

    @property
    def keywords(self) -> List[str]:
        return ["aws", "s3", "ec2", "lambda", "iam", "rds", "dynamodb"]

    async def run_aws_command(self, command: str) -> str:
        """Execute an AWS CLI command asynchronously.

        Args:
            command (str): The AWS CLI command to execute (without 'aws' prefix)

        Returns:
            str: The command output or error message
        """
        try:
            # Split the command into parts and add 'aws' at the beginning
            cmd_parts = ['aws'] + shlex.split(command)
            # Run the AWS CLI command
            result = subprocess.run(cmd_parts, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error: {result.stderr}"
        except Exception as e:
            return f"Error executing AWS command: {str(e)}"

    async def arun(self, command: str) -> str:
        """Async wrapper for run_aws_command."""
        return await self.run_aws_command(command)

    def run(self, command: str) -> str:
        """Sync wrapper for run_aws_command."""
        return asyncio.run(self.run_aws_command(command))


def create_aws_cli_tool() -> Tool:
    """Create and configure an AWS CLI tool.

    Returns:
        Tool: Configured AWS CLI tool
    """
    aws_cli = AWSCliTool()
    return Tool(
        name=aws_cli.name,
        description=aws_cli.description,
        func=aws_cli.run,
        coroutine=aws_cli.arun
    )

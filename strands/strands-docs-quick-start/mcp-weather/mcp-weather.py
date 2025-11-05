
# This does noot work unless server-weather.py is running
# for example, from the repo that ships it: 
# python mcp-streamable-http/python-example/server/weather.py).
from strands import Agent, tool
from strands.tools.mcp.mcp_client import MCPClient
from mcp.client.streamable_http import streamablehttp_client

from strands.models import BedrockModel

model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
model = BedrockModel(
    model_id=model_id,
)

# Pre-req, run the following to start the streamable Http server, in a different terminal:
# python mcp-streamable-http/python-example/server/weather.py
streamable_http_mcp_client = MCPClient(
    lambda: streamablehttp_client(
        url="http://localhost:8123/mcp"
    ))

# Create an agent with MCP tools
with streamable_http_mcp_client:
    # Get the tools from the MCP server
    tools = streamable_http_mcp_client.list_tools_sync()

    # Create an agent with these tools
    agent = Agent(
        system_prompt="You are weather expert, provide weather details by using the available tools",
        model=model, 
        tools=tools
        )
    agent("What is weather in New York?")
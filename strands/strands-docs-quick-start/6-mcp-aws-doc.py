 
from strands import Agent, tool
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters
from strands.models import BedrockModel

model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
model = BedrockModel(
    model_id=model_id,
)



# Connect to an MCP server using stdio transport
# Note: uvx command syntax differs by platform

# For macOS/Linux:
stdio_mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="uvx", 
        args=["awslabs.aws-documentation-mcp-server@latest"]
    )
))

# For Windows:
# stdio_mcp_client = MCPClient(lambda: stdio_client(
#     StdioServerParameters(
#         command="uvx", 
#         args=[
#             "--from", 
#             "awslabs.aws-documentation-mcp-server@latest", 
#             "awslabs.aws-documentation-mcp-server.exe"
#         ]
#     )
# ))

# Create an agent with MCP tools
with stdio_mcp_client:
    # Get the tools from the MCP server
    tools = stdio_mcp_client.list_tools_sync()

    # Create an agent with these tools
    agent = Agent(
        system_prompt="You are an AWS Documentation expert. Use the tools are are available to provide factual information",
        model=model, 
        tools=tools
        )
    agent("What is AWS Lambda?")
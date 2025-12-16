https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-mcp.html

Deploy to agentcore runtime

uv add bedrock-agentcore-starter-toolkit

Note: create __init__.py to make the directory a python package

agentcore configure -e my_mcp_server.py --protocol MCP

agentcore launch

Note: To access MCP server in agentcore you need agent_arn and bearer_token
The bearer_token can be extracted using cognito, autho,...
 
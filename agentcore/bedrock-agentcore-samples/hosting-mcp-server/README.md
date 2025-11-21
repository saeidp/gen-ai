https://github.com/awslabs/amazon-bedrock-agentcore-samples/blob/main/01-tutorials/01-AgentCore-runtime/02-hosting-MCP-server/hosting_mcp_server_iam_auth.ipynb

Mcp_client_local connect to mcp_server locally. You can test it before deploying to agentcore

The other mcp files are all for testing the agent core mcp server

In the launch process

You may encounter build error and the fix is as follows
CodeBuild was failing during uv pip install . because setuptools couldn’t auto-discover the package in the flat layout: it saw multiple top-level modules (mcp_client, mcp_server) and aborted with “Multiple top-level modules discovered”. Adding [tool.setuptools] py-modules = ["mcp_server", "mcp_client"] in pyproject.toml explicitly told it what to include, so the build succeeded and the agent deployed.

If you want, you can now hit the AgentCore MCP endpoint or run the local mcp_client.py to confirm the tools list.

python mcp_client_remote.py \
  --region ap-southeast-2 \
  --runtime-arn arn:aws:bedrock-agentcore:ap-southeast-2:381491838394:runtime/mcp_server_iam-BH1RwGAovj \
  --name "TestUser"

(without --name it just lists tools).

Ypo can also get the region and arn in the code if you dont send them
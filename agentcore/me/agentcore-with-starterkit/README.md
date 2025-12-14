https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-get-started-code-deploy.html

uv add bedrock-agentcore strands-agents
uv add --dev bedrock-agentcore-starter-toolkit

uv run main.py

curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello!"}'

uv run agentcore configure -e main.py -n agent_name # provides an interactive CLI to configure

Deployment Configuration
Select deployment type:
 1. Code Zip (recommended) - Python only, no Docker required
 2. Container - For custom runtimes or complex dependencies
or
uv run agentcore configure -e main.py --deployment_type direct_code_deploy
or
uv run agentcore configure -e main.py --deployment_type container

uv run agentcore launch

uv run agentcore invoke '{"prompt":"Tell me a joke"}'


Delete all resources related to agentcore runtime
uv run agentcore destroy

s3 artifacts and agentcore execution role will be deleted

Note: If uing direct_code_deploy then the following folder is created
.bedrock_agentcore/direct_agent with the following files
1. dependencies.hash
2. dependencies.zip
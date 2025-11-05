# This code is extracted from 
 https://builder.aws.com/content/33duot88gLusLRgJkalulTJLUrx/turn-your-ai-script-into-a-production-ready-agent

# Please make sure you rename tutorial_agent-* to tutorial_agent and then do the followings
# This tutorial_agent-.agentCoreCodeInterpreter.py have issues with agentcore version and did not configured correctly

# From your main project directory (agentcore-tutorial)
# Configure the agent:
uv run agentcore configure -e agent_deployment/tutorial_agent.py

# Deploy to production
uv run agentcore launch

# Test your deployed agent
uv run agentcore invoke '{"prompt": "What is 25 * 4 + 10?"}'

uv run agentcore status

# Memory
# Session 1: Store user preferences (using memory)
uv run agentcore invoke '{"prompt": "Remember that I absolutely love hot tea, especially Earl Grey, and I prefer it with a splash of milk and one sugar"}' --session-id 12345-12345-12345-12345-12345-12345-A --headers "Actor-Id:user123"

# Session 2: Different session, retrieve the preferences
uv run agentcore invoke '{"prompt": "What kind of hot drinks do I like and how do I prefer them prepared?"}' --session-id 12345-12345-12345-12345-12345-12345-B --headers "Actor-Id:user123"

If problem then add the following in the .bedrock_agentcore.yaml
request_header_configuration:
      requestHeaderAllowlist:
      - X-Amzn-Bedrock-AgentCore-Runtime-Custom-Actor-Id


# agent_core_code_interpreter
# Configure and deploy
uv --directory ./agent_deployment add strands-agents-tools[agent_core_code_interpreter]
uv run agentcore configure -e agent_deployment/tutorial_agent.py
uv run agentcore launch

# Check status and note the observability dashboard URL
uv run agentcore status



# how do you invoke your agent from production applications?
```python
import boto3
import json

# Initialize the AgentCore client
client = boto3.client('bedrock-agentcore', region_name='us-west-2')

# Get your agent ARN from: uv run agentcore status
agent_arn = "arn:aws:bedrock-agentcore:us-west-2:123456789012:runtime/your-agent-name"

# Invoke the agent
response = client.invoke_agent_runtime(
    agentRuntimeArn=agent_arn,
    runtimeSessionId="production_session_2024_user456_webapp_xyz123",
    payload=b'{"prompt": "What is 25 * 4 + 10?"}'
)

# Parse the response
result = json.loads(response['response'].read())
print(result['response'])
```

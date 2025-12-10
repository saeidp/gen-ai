from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel

app = BedrockAgentCoreApp()
model_id = "global.anthropic.claude-haiku-4-5-20251001-v1:0"

model = BedrockModel(
    model_id=model_id,
)
agent = Agent(
    model=model,
)

@app.entrypoint
def invoke(payload):
    """Your AI agent function"""
    user_message = payload.get("prompt", "Hello! How can I help you today?")
    result = agent(user_message)
    return {"result": result.message}

if __name__ == "__main__":
    app.run()


#  uv run 1-test_agentcore_local.py
#  Then send a POST request to http://localhost:8000/invokations with JSON body {"prompt": "Your message here"}

#  Test Locally 
#  Open another terminal and use curl to test:
#  curl -X POST http://localhost:8080/invocations \
#   -H "Content-Type: application/json" \
#   -d '{"prompt": "Hello!"}'

#  Configure the agent for deploying to agentcore
#  uv run agentcore configure -e my_agent.py
#  uv run agentcore launch

#  How to test after deployment:
#  uv run agentcore invoke '{"prompt": "tell me a joke"}' 
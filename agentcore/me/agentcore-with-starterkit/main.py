from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel

app = BedrockAgentCoreApp(debug=True)

model_id = "global.anthropic.claude-haiku-4-5-20251001-v1:0"
model = BedrockModel(model_id=model_id)

agent = Agent(model=model)

@app.entrypoint
def invoke(payload):
    """Your AI agent function"""
    user_message = payload.get("prompt", "Hello! How can I help you today?")
    app.logger.info(f"User message: {user_message}")
    result = agent(user_message)
    return {"result": result.message}

if __name__ == "__main__":
    app.run()
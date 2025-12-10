from strands import Agent, tool
from strands_tools import calculator # Import the calculator tool
import argparse
import json
from strands.models import BedrockModel
from bedrock_agentcore.runtime import BedrockAgentCoreApp


app = BedrockAgentCoreApp()
# Create a custom tool 
@tool
def weather():
    """ Get weather """ # Dummy implementation
    return "sunny"


model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
model = BedrockModel(
    model_id=model_id,
)
agent = Agent(
    model=model,
    tools=[calculator, weather],
    system_prompt="You're a helpful assistant. You can do simple math calculation, and tell the weather."
)

@app.entrypoint
def strands_agent_bedrock(payload):
    """
    Invoke the agent with a payload
    """
    user_input = payload.get("prompt")
    response = agent(user_input)
    return response.message['content'][0]['text']

if __name__ == "__main__":
    app.run()


    # parser = argparse.ArgumentParser()
    # # Make payload optional so the runtime can import/execute the module
    # # without providing CLI args. When provided, it should be a JSON string.
    # parser.add_argument("payload", nargs="?", type=str, default=None)
    # args = parser.parse_args()
    # if args.payload:
    #     # Called from CLI with a payload JSON string
    #     response = strands_agent_bedrock(json.loads(args.payload))
    #     # Print the response so CLI users see output
    #     try:
    #         print(response)
    #     except Exception:
    #         pass
    # else:
    #     # No payload provided (e.g. AgentCore runtime started the module).
    #     # Do nothing; the runtime will invoke the agent via the exposed
    #     # `strands_agent_bedrock` function / HTTP entrypoint.
    #     pass

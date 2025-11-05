from strands import Agent
from strands_tools import calculator
from strands.models import BedrockModel

model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
model = BedrockModel(
    model_id=model_id,
)
agent = Agent(
    model = model,
    tools=[calculator]
 
)

result = agent( "Calculate 25 * 48")

print("\n----------------------\n" )
print(result.message)

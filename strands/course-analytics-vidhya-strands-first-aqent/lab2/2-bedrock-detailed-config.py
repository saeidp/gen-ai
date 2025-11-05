from strands import Agent
from strands.models import BedrockModel

# Configure specific Bedrock model
bedrock_model = BedrockModel(
    model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",  # Specify the model
    temperature=0.3,                         # Control randomness
    top_p=0.8,                              # Control token selection
    streaming=True                           # Enable response streaming
)

agent = Agent(model=bedrock_model)

response = agent("Tell me about Amazon Bedrock")


# Import the Agent class from the strands package
# The Agent class provides AI capabilities for question answering and other tasks
from strands import Agent
from strands.models import BedrockModel

model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
model = BedrockModel(
    model_id=model_id,
)
agent = Agent(
    model=model,
    system_prompt="You're a helpful assistant. You can do simple math calculation, and tell the weather."
)
# Ask the agent a question by calling the agent instance like a function
# The agent will process the question and return a response
response = agent("What is Agentic AI?")

# Note: You can ask different types of questions by changing the string passed to the agent
# For example: agent("What is the capital of France?")
# or agent("Explain how photosynthesis works")
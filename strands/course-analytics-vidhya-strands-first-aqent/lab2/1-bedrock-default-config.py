from strands import Agent

# Uses Bedrock with Claude 4 Sonnet by default
# you must have access to the model in your AWS account
agent = Agent()
response = agent("Tell me about Amazon Bedrock")
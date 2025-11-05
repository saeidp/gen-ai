from strands import Agent
from bedrock_agentcore import BedrockAgentCoreApp
from strands_tools import current_time, http_request, use_aws

from strands.models import BedrockModel
model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
model = BedrockModel(
    model_id=model_id,
)

app = BedrockAgentCoreApp()

WETHER_SYSTEM_PROMPT = """You are a weather assistant with http capabilities. You can":
- Make HTTP request to the National weather service API
- Process and display weather forecast data
- Provides weather information for locations in the united states

When displaying responses:
- Format weather data in a human-readble way
- Highlight important information like temerature, percipitation, and alerts
- Handle errors appropriately
- convert technical terms to user friendly language

Always explain the weather condition clearly and provide context for forcast.
"""

agent = Agent(
    model= model,
    tools = [current_time, http_request, use_aws],
    system_prompt= WETHER_SYSTEM_PROMPT
)

@app.entrypoint
def invoke(payload0):
    query= """
    Answere the following questions. Please answere them all:
    1- what is the time in new york city, USA?
    2- what is the weather in new york city, USA?    
    """ # 3- list the s3 bucket in my aws account
    response = agent(query)
    return {"result": response.message}

if __name__ == "__main__":
    app.run()
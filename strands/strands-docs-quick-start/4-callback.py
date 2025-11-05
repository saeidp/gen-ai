# Here is an example that captures streamed data from the agent 
# and logs it instead of printing:
import json
import logging
from strands import Agent
from strands_tools import shell
from strands.models import BedrockModel

model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
model = BedrockModel(
    model_id=model_id,
)

logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
)

logging.getLogger("strands").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

# logger = logging.getLogger("my_agent")

# Define a simple callback handler that logs instead of printing
tool_use_ids = []
def callback_handler(**kwargs):
    if "data" in kwargs:
        # Log the streamed data chunks
        logger.info(kwargs["data"].rstrip("\n"))
    elif "current_tool_use" in kwargs:
        tool = kwargs["current_tool_use"]
        if tool["toolUseId"] not in tool_use_ids:
            # Log the tool use
            logger.info(f"\n[Using tool: {tool.get('name')}]")
            tool_use_ids.append(tool["toolUseId"])

# Create an agent with the callback handler
agent = Agent(
    model=model,
    tools=[shell],
    callback_handler=callback_handler
)

# Ask the agent a question
# make sure you run it in an admin shell to allow shell access
result = agent("What operating system am I using?")

# Print only the last response
print(result.message)
print("\n ---------------------- \n")
print(tool_use_ids)

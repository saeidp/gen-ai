import json
import logging

from strands import Agent
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

logging.getLogger("strands").setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

agent = Agent(model=model)
logger.info("Bedrock model config: %s", json.dumps(agent.model.config, indent=2))
agent("Hello, world!")

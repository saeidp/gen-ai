
# A2AServer wraps the agent to provide A2A protocol compatibility
# Agent Card URL dynamically constructs the correct URL based on deployment
# context using the AGENTCORE_RUNTIME_URL environment variable
#  Port 9000 A2A servers run on port 9000 by default in AgentCore Runtime
import logging  
import os  
from strands_tools.calculator import calculator  
from strands import Agent  
from strands.multiagent.a2a import A2AServer  
from strands.models import BedrockModel
import uvicorn  
from fastapi import FastAPI  

model_id= "global.anthropic.claude-haiku-4-5-20251001-v1:0"
# model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
model = BedrockModel(
    model_id=model_id,
)

logging.basicConfig(level=logging.INFO)  

# Use the complete runtime URL from environment variable, fallback to local  
runtime_url = os.environ.get('AGENTCORE_RUNTIME_URL', 'http://127.0.0.1:9000/')  

logging.info(f"Runtime URL: {runtime_url}")  

strands_agent = Agent(
    model=model,  
    name="Calculator Agent",  
    description="A calculator agent that can perform basic arithmetic operations.",  
    tools=[calculator],  
    callback_handler=None  
)  

host, port = "0.0.0.0", 9000  

# Pass runtime_url to http_url parameter AND use serve_at_root=True  
a2a_server = A2AServer(  
    agent=strands_agent,  
    http_url=runtime_url,  
    serve_at_root=True  # Serves locally at root (/) regardless of remote URL path complexity  
)  

app = FastAPI()  

@app.get("/ping")  
def ping():  
    return {"status": "healthy"}  

app.mount("/", a2a_server.to_fastapi_app())  

if __name__ == "__main__":
    # Start the Uvicorn server with the FastAPI app  
    uvicorn.run(app, host=host, port=port)


# Invoke agent
#  curl -X POST http://localhost:9000/ \
# -H "Content-Type: application/json" \
# -d '{  
#   "jsonrpc": "2.0",  
#   "id": "req-001",  
#   "method": "message/send",  
#   "params": {  
#     "message": {  
#       "role": "user",  
#       "parts": [  
#         {  
#           "kind": "text",  
#           "text": "what is 101 * 11?"  
#         }  
#       ],  
#       "messageId": "12345678-1234-1234-1234-123456789012"  
#     }  
#   } 
# }' | jq . 

# Test agent card retrieval
# curl http://localhost:9000/.well-known/agent-card | jq .
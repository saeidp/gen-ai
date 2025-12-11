# This implementation:
# Creates a FastAPI application with the required endpoints
# Initializes a Strands agent for processing user messages
# Implements the /invocations POST endpoint for agent interactions
# Implements the /ping GET endpoint for health checks
# Configures the server to run on host 0.0.0.0 and port 8080
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
from strands import Agent
from strands.models import BedrockModel

app = FastAPI(title="Strands Agent Server", version="1.0.0")

# Initialize Strands agent
model_id = "global.anthropic.claude-haiku-4-5-20251001-v1:0"

model = BedrockModel(
    model_id=model_id,
)

strands_agent = Agent(model=model)

class InvocationRequest(BaseModel):
    input: Dict[str, Any]

class InvocationResponse(BaseModel):
    output: Dict[str, Any]

@app.post("/invocations", response_model=InvocationResponse)
async def invoke_agent(request: InvocationRequest):
    try:
        user_message = request.input.get("prompt", "")
        if not user_message:
            raise HTTPException(
                status_code=400, 
                detail="No prompt found in input. Please provide a 'prompt' key in the input."
            )

        result = strands_agent(user_message)
        response = {
            "message": result.message,
            "timestamp": datetime.utcnow().isoformat()
        }

        return InvocationResponse(output=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent processing failed: {str(e)}")

@app.get("/ping")
async def ping():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

# Test Locally for getting health status
# uv run uvicorn agent:app --host 0.0.0.0 --port 8080
# In another terminal window
# curl http://localhost:8080/ping

#  Invocations (test for agent interaction)
#  In another terminal window, you can test the server with:
# curl -X POST http://localhost:8080/invocations \
#   -H "Content-Type: application/json" \
#   -d '{
#     "input": {"prompt": "What is artificial intelligence?"}
#   }'
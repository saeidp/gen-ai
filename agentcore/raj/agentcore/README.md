Packages:
"bedrock-agentcore-starter-toolkit>=0.1.26",
"bedrock-agentcore>=1.0.3",
"strands-agents>=1.13.0",
"strands-agents-tools>=0.2.12",

Configure and Run from Server
uv run agentcore configure -e agent-core.py
uv run agentcore launch
uv run agentcore invoke '{"prompt": "Hello"}'
uv run agentcore destroy

Run Locally:
uv run agentcore configure -e agent-core.py
uv run agentcore launch --local
uv run agentcore invoke --local '{"prompt": "Hello"}'
or
curl -X POST http://127.0.0.1:8080/invocations \
     -H 'Content-Type: application/json' \
     -d '{}'



Note: If you want the third question about AWS works correctly you need to 
give the role readonly access to the s3.
Role name is inside the file .bedrock_agentcore.yaml

Note: 
You only need to rerun agentcore configure when something about the configuration changes—entrypoint path, requirements, AWS settings, etc. Ordinary code edits inside 0-Raj/agent-core.py don’t require another configure step.

After changing the code, just redeploy with uv run agentcore launch; the CLI rebuilds the package and pushes the new version using the existing config. If you ever move the file, rename it, or tweak dependency files, then rerun uv run agentcore configure -e ./0-Raj/agent-core.py before launching again.

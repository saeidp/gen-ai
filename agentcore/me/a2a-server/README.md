https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a.html

Amazon Bedrock AgentCore's A2A protocol support enables seamless integration with A2A servers by acting as a transparent proxy layer. When configured for A2A, Amazon Bedrock AgentCore expects containers to run stateless, streamable HTTP servers on port 9000 at the root path (0.0.0.0:9000/), which aligns with the default A2A server configuration.

This architecture preserves the standard A2A protocol features like built-in agent discovery through Agent Cards at /.well-known/agent-card.json and JSON-RPC communication, while adding enterprise authentication (SigV4/OAuth 2.0) and scalability.

The key differentiators from other protocols are the port (9000 vs 8080 for HTTP), mount path (/ vs /invocations), and the standardized agent discovery mechanism, making Amazon Bedrock AgentCore an ideal deployment platform for A2A agents in production environments.

by following the above link you can deploy the agent to the agentcore runtime

agentcore configure -e my_a2a_server.py --protocol A2A
agentcore launch

You need both the Bearer_token and agent_arn
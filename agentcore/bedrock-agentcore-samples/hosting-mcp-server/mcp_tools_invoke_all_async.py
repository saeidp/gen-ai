import asyncio, json, urllib.parse, sys
import boto3, httpx
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

async def post_signed_async(url, region, payload, extra_headers=None):
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if extra_headers: headers.update(extra_headers)
    creds = boto3.Session().get_credentials().get_frozen_credentials()
    req = AWSRequest(method="POST", url=url, data=json.dumps(payload), headers=headers)
    SigV4Auth(creds, "bedrock-agentcore", region).add_auth(req)
    async with httpx.AsyncClient() as client:
        return await client.post(url, headers=dict(req.headers), content=req.body)

async def main():
    region = boto3.Session().region_name
    ssm = boto3.client("ssm", region_name=region)
    agent_arn = ssm.get_parameter(Name="/mcp_server/runtime_iam/agent_arn")["Parameter"]["Value"]
    url = f"https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{urllib.parse.quote(agent_arn,safe='')}/invocations?qualifier=DEFAULT"

    resp = await post_signed_async(url, region, {"jsonrpc":"2.0","id":1,"method":"sessions/create","params":{"protocolVersion":"2025-06-18"}})
    session_id = resp.headers.get("mcp-session-id")
    print("Create session:", resp.status_code, resp.text)
    if not session_id: sys.exit(1)

    resp2 = await post_signed_async(url, region, {"jsonrpc":"2.0","id":2,"method":"tools/list"}, {"Mcp-Session-Id":session_id})
    print("List:", resp2.status_code, resp2.text)

    async def call(name, args):
        r = await post_signed_async(url, region, {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":name,"arguments":args}}, {"Mcp-Session-Id":session_id})
        print(name, r.status_code, r.text)
    await call("add_numbers", {"a":5,"b":3})
    await call("multiply_numbers", {"a":4,"b":7})
    await call("greet_user", {"name":"Alice"})

if __name__ == "__main__":
    asyncio.run(main())

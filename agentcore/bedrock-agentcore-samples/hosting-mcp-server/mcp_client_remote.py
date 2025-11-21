import argparse
import json
import sys
import urllib.parse

import boto3
import httpx
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest


def sign_request(url: str, region: str, payload: str, extra_headers: dict[str, str] | None = None) -> AWSRequest:
    """Sign a bedrock-agentcore InvokeRuntime request with SigV4."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if extra_headers:
        headers.update(extra_headers)

    creds = boto3.Session().get_credentials().get_frozen_credentials()
    req = AWSRequest(method="POST", url=url, data=payload, headers=headers)
    SigV4Auth(creds, "bedrock-agentcore", region).add_auth(req)
    return req


def post_signed(url: str, region: str, payload: dict, extra_headers: dict[str, str] | None = None) -> httpx.Response:
    signed_req = sign_request(url, region, json.dumps(payload), extra_headers)
    with httpx.Client() as client:
        return client.post(url, headers=dict(signed_req.headers), content=signed_req.body)


def create_session(url: str, region: str) -> tuple[httpx.Response, str | None]:
    payload = {"jsonrpc": "2.0", "id": 1, "method": "sessions/create", "params": {"protocolVersion": "2025-06-18"}}
    resp = post_signed(url, region, payload)
    return resp, resp.headers.get("mcp-session-id")


def list_tools(url: str, region: str, session_id: str) -> httpx.Response:
    payload = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
    return post_signed(url, region, payload, extra_headers={"Mcp-Session-Id": session_id})


def call_greet(url: str, region: str, session_id: str, name: str) -> httpx.Response:
    payload = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {"name": "greet_user", "arguments": {"name": name}},
    }
    return post_signed(url, region, payload, extra_headers={"Mcp-Session-Id": session_id})


def main():
    parser = argparse.ArgumentParser(description="MCP client using SigV4 to list tools and optionally greet")
    parser.add_argument("--region", required=False, help="Runtime region, e.g., ap-southeast-2")
    parser.add_argument("--runtime-arn", required=False, help="Runtime ARN (bedrock-agentcore)")
    parser.add_argument("--qualifier", default="DEFAULT", help="Qualifier/version (default: DEFAULT)")
    parser.add_argument("--name", help="Name to greet (optional)")
    args = parser.parse_args()

    region = args.region
    if not args.region:
        boto_session = boto3.Session()
        region = boto_session.region_name
        print(f"Using AWS region: {region}")


    runtime_arn = args.runtime_arn
    if not runtime_arn:
        ssm_client = boto3.client("ssm", region_name=region)
        agent_arn_response = ssm_client.get_parameter(
        Name="/mcp_server/runtime_iam/agent_arn"
        )
        runtime_arn = agent_arn_response["Parameter"]["Value"]
        print(f"Retrieved Agent ARN: {runtime_arn}")


    encoded = urllib.parse.quote(runtime_arn, safe="")
    url = f"https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{encoded}/invocations?qualifier={args.qualifier}"

    # Create session
    print(f"Creating session to {url}")
    resp, session_id = create_session(url, region)
    print("Session status:", resp.status_code)
    print("Request ID:", resp.headers.get("x-amzn-requestid"))
    print("MCP Session ID:", session_id)
    print("Body:", resp.text or repr(resp.content))

    if resp.status_code != 200 or not session_id:
        print("Failed to create session; aborting.")
        sys.exit(1)

    # List tools
    print("\nListing tools...")
    resp2 = list_tools(url, region, session_id)
    print("List status:", resp2.status_code)
    print("Request ID:", resp2.headers.get("x-amzn-requestid"))
    print("Body:", resp2.text or repr(resp2.content))

    # Optionally call greet_user
    if args.name:
        print(f"\nCalling greet_user with name={args.name}...")
        resp3 = call_greet(url, region, session_id, args.name)
        print("Call status:", resp3.status_code)
        print("Request ID:", resp3.headers.get("x-amzn-requestid"))
        print("Body:", resp3.text or repr(resp3.content))


if __name__ == "__main__":
    main()

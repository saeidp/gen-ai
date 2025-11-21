"""
Invoke MCP tools on the AgentCore runtime using simple SigV4-signed HTTP calls.

This mirrors the working approach from mcp_list_tools.py/mcp_call_greet.py.
It:
  - Fetches the runtime ARN from SSM (parameter /mcp_server/runtime_iam/agent_arn)
  - Creates an MCP session
  - Lists tools
  - Calls add_numbers, multiply_numbers, and greet_user
"""

from __future__ import annotations

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


def create_session(url: str, region: str):
    payload = {"jsonrpc": "2.0", "id": 1, "method": "sessions/create", "params": {"protocolVersion": "2025-06-18"}}
    return post_signed(url, region, payload)


def list_tools(url: str, region: str, session_id: str):
    payload = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
    return post_signed(url, region, payload, extra_headers={"Mcp-Session-Id": session_id})


def call_tool(url: str, region: str, session_id: str, name: str, arguments: dict):
    payload = {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": name, "arguments": arguments}}
    return post_signed(url, region, payload, extra_headers={"Mcp-Session-Id": session_id})


def main():
    boto_session = boto3.Session()
    region = boto_session.region_name
    print(f"Using AWS region: {region}")

    ssm_client = boto3.client("ssm", region_name=region)
    agent_arn = ssm_client.get_parameter(Name="/mcp_server/runtime_iam/agent_arn")["Parameter"]["Value"]
    print(f"Retrieved Agent ARN: {agent_arn}")

    if not agent_arn:
        print("❌ Error: AGENT_ARN not found")
        sys.exit(1)

    encoded = urllib.parse.quote(agent_arn, safe="")
    url = f"https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{encoded}/invocations?qualifier=DEFAULT"

    # 1) Create session
    print("\n🔄 Initializing MCP session...")
    resp = create_session(url, region)
    session_id = resp.headers.get("mcp-session-id")
    print("Session status:", resp.status_code)
    print("Request ID:", resp.headers.get("x-amzn-requestid"))
    print("MCP Session ID:", session_id)
    print("Body:", resp.text or repr(resp.content))
    if resp.status_code != 200 or not session_id:
        print("Failed to create session; aborting.")
        sys.exit(1)

    # 2) List tools
    print("\n🔄 Listing tools...")
    resp2 = list_tools(url, region, session_id)
    print("List status:", resp2.status_code)
    print("Request ID:", resp2.headers.get("x-amzn-requestid"))
    print("Body:", resp2.text or repr(resp2.content))
    if resp2.status_code != 200:
        print("Failed to list tools; aborting.")
        sys.exit(1)

    # 3) Call tools
    def do_call(name: str, args: dict):
        print(f"\n🧪 Calling {name} with {args} ...")
        r = call_tool(url, region, session_id, name, args)
        print("Status:", r.status_code)
        print("Request ID:", r.headers.get("x-amzn-requestid"))
        print("Body:", r.text or repr(r.content))

    do_call("add_numbers", {"a": 5, "b": 3})
    do_call("multiply_numbers", {"a": 4, "b": 7})
    do_call("greet_user", {"name": "Alice"})

    print("\n✅ MCP tool testing completed!")


if __name__ == "__main__":
    main()

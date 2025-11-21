"""
Call the `greet_user` MCP tool via SigV4-signed requests.

Usage:
  python mcp_call_greet.py \
    --region ap-southeast-2 \
    --runtime-arn arn:aws:bedrock-agentcore:ap-southeast-2:123456789012:runtime/your-runtime \
    --name "TestUser"

Requirements:
  - AWS credentials in your environment/profile with permission to InvokeRuntime.
  - httpx, boto3, botocore available (already in this project).
"""

from __future__ import annotations

import argparse
import json
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


def call_greet(url: str, region: str, session_id: str, name: str) -> httpx.Response:
    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {"name": "greet_user", "arguments": {"name": name}},
    }
    return post_signed(url, region, payload, extra_headers={"Mcp-Session-Id": session_id})


def main():
    parser = argparse.ArgumentParser(description="Call greet_user tool via AgentCore runtime")
    parser.add_argument("--region", required=True, help="Runtime region, e.g., ap-southeast-2")
    parser.add_argument("--runtime-arn", required=True, help="Runtime ARN (bedrock-agentcore)")
    parser.add_argument("--qualifier", default="DEFAULT", help="Qualifier/version (default: DEFAULT)")
    parser.add_argument("--name", required=True, help="Name to greet")
    args = parser.parse_args()

    encoded = urllib.parse.quote(args.runtime_arn, safe="")
    url = f"https://bedrock-agentcore.{args.region}.amazonaws.com/runtimes/{encoded}/invocations?qualifier={args.qualifier}"

    print(f"Creating session to {url}")
    resp, session_id = create_session(url, args.region)
    print("Session status:", resp.status_code)
    print("Request ID:", resp.headers.get("x-amzn-requestid"))
    print("MCP Session ID:", session_id)
    print("Body:", resp.text or repr(resp.content))

    if resp.status_code != 200 or not session_id:
        print("Failed to create session; aborting.")
        return

    print("\nCalling greet_user...")
    resp2 = call_greet(url, args.region, session_id, args.name)
    print("Call status:", resp2.status_code)
    print("Request ID:", resp2.headers.get("x-amzn-requestid"))
    print("Body:", resp2.text or repr(resp2.content))


if __name__ == "__main__":
    main()

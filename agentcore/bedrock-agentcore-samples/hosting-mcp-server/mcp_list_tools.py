"""
Simple script to list tools from the deployed MCP runtime using SigV4 auth.

Usage:
  python mcp_list_tools.py \
    --region ap-southeast-2 \
    --runtime-arn arn:aws:bedrock-agentcore:ap-southeast-2:123456789012:runtime/your-runtime-name

Requirements:
  - Your AWS credentials (profile/SSO/ENV) must be able to InvokeRuntime.
  - httpx, boto3, botocore installed (already in this project).
"""

from __future__ import annotations

import argparse
import json
import urllib.parse

import boto3
import httpx
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest


def sign_request(url: str, region: str, payload: str, extra_headers: dict[str, str] | None = None):
    """Sign the request for bedrock-agentcore Invocations with SigV4."""
    # Accept must include both JSON and SSE for MCP compatibility.
    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if extra_headers:
        base_headers.update(extra_headers)

    creds = boto3.Session().get_credentials().get_frozen_credentials()
    req = AWSRequest(method="POST", url=url, data=payload, headers=base_headers)
    SigV4Auth(creds, "bedrock-agentcore", region).add_auth(req)
    return req


def post_signed(url: str, region: str, payload: dict, extra_headers: dict[str, str] | None = None) -> httpx.Response:
    signed = sign_request(url, region, json.dumps(payload), extra_headers)
    with httpx.Client() as client:
        return client.post(url, headers=dict(signed.headers), content=signed.body)


def create_session(url: str, region: str) -> httpx.Response:
    payload = {"jsonrpc": "2.0", "id": 1, "method": "sessions/create", "params": {"protocolVersion": "2025-06-18"}}
    return post_signed(url, region, payload)


def list_tools(url: str, region: str, session_id: str) -> httpx.Response:
    payload = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
    return post_signed(url, region, payload, extra_headers={"Mcp-Session-Id": session_id})


def main():
    parser = argparse.ArgumentParser(description="List MCP tools from AgentCore runtime")
    parser.add_argument("--region", required=True, help="AWS region of the runtime (e.g., ap-southeast-2)")
    parser.add_argument("--runtime-arn", required=True, help="Runtime ARN, e.g., arn:aws:bedrock-agentcore:...:runtime/...")
    parser.add_argument("--qualifier", default="DEFAULT", help="Qualifier/version (default: DEFAULT)")
    args = parser.parse_args()

    encoded = urllib.parse.quote(args.runtime_arn, safe="")
    url = f"https://bedrock-agentcore.{args.region}.amazonaws.com/runtimes/{encoded}/invocations?qualifier={args.qualifier}"

    # 1) Create session
    print(f"Creating session to {url}")
    resp = create_session(url, args.region)
    print("Session status:", resp.status_code)
    print("Request ID:", resp.headers.get("x-amzn-requestid"))
    session_id = resp.headers.get("mcp-session-id")
    print("MCP Session ID:", session_id)
    print("Body:", resp.text or repr(resp.content))

    if resp.status_code != 200 or not session_id:
        print("Failed to create session; aborting.")
        return

    # 2) List tools
    print("\nListing tools...")
    resp2 = list_tools(url, args.region, session_id)
    print("List status:", resp2.status_code)
    print("Request ID:", resp2.headers.get("x-amzn-requestid"))
    print("Body:", resp2.text or repr(resp2.content))


if __name__ == "__main__":
    main()

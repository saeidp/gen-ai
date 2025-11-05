# Import necessary libraries
import os                                     # For accessing environment variables
from strands import Agent                    # Import the Agent class from strands library
from strands_tools import use_aws           # Import the AWS tool for interacting with AWS services
from strands.models import BedrockModel

# Configure specific Bedrock model
model = BedrockModel(
    # boto_session=boto3.Session(),          # Reuse an existing boto3 session
    # boto_client_config=BotocoreConfig(),   # Customize retry, timeouts, or user agent
    # region_name="us-west-2",              # Override AWS region (defaults to env/AWS config)
    # endpoint_url="https://...",           # Point at a VPC or custom Bedrock endpoint
    model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",  # Specify the model
    temperature=0.3,                         # Control randomness
    top_p=0.8,
    max_tokens=1028,                         # Control token selection
    # additional_args={},                     # Extra provider-specific params for each request
    # additional_request_fields={},           # Inject raw fields into the Bedrock request payload
    # additional_response_field_paths=[],     # Extract extra fields from the Bedrock response
    # cache_prompt="my-cache",                # Tag for Bedrock prompt caching
    # cache_tools="my-cache",                 # Tag for Bedrock tool caching
    # guardrail_id="gr-123",                  # Bedrock guardrail ID to enforce
    # guardrail_version="1",                  # Guardrail version if multiple exist
    # guardrail_trace="enabled",              # Guardrail trace mode: "enabled", "disabled", "enabled_full"
    # guardrail_stream_processing_mode="sync",  # Guardrail processing: "sync" or "async"
    # guardrail_redact_input=True,             # Redact the prompt when guardrails trigger
    # guardrail_redact_input_message="Input removed",   # Replacement text when input is redacted
    # guardrail_redact_output=False,           # Redact the completion when guardrails trigger
    # guardrail_redact_output_message="Output removed", # Replacement text when output is redacted
    # include_tool_result_status="auto",      # Force tool result status True/False or let library decide
    # stop_sequences=["</done>"],              # Stop generation when any sequence is produced
    # streaming=True,                         # Enable token-by-token streaming responses
)

# Create an AI agent with AWS capabilities
agent = Agent(
    model=model,                      # Use the Anthropic model configured above
    tools=[use_aws]                   # Give the agent access to AWS tools for interacting with AWS services
)

# Example queries (toggle line comments to enable)

query= "List the S3 buckets in my account"  # Simple query to list S3 buckets in the configured AWS account

# query= "How many s3 buckets does exist in my account"  # Simple query to list S3 buckets in the configured AWS account


#query="Query the DynamoDB table called 'UserProfiles' in the us-west-2 region. Get all items for userId 'user123' and show me the results in a readable format."  # Query for a specific user in DynamoDB

#query="Find all users in the 'UserProfiles' table in the us-west-2 region who have an attribute 'status' of 'Active', show me their names and email addresses."

# Send the query to the agent and store the response
# The agent will use the use_aws tool to interact with DynamoDB and S3  and filter the results
response = agent(query)

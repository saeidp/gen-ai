// Import the required AWS SDK client for Bedrock
import { BedrockRuntimeClient, InvokeModelCommand } from "@aws-sdk/client-bedrock-runtime";

// Initialize the Bedrock client
const client = new BedrockRuntimeClient({ region: 'ap-southeast-2' });  // Adjust to your region

async function invokeClaude3Haiku(prompt) {
    const command = new InvokeModelCommand({
        modelId: 'anthropic.claude-3-haiku-20240307-v1:0',  // Model ID for Claude 3 Haiku
        contentType: 'application/json',
        accept: 'application/json',
        body: JSON.stringify({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": [{
                        "type": "text",
                        "text": prompt
                      }]
                }
            ]
            
        })
    });

    try {
        // Send the request to the Bedrock model and wait for the response
        const response = await client.send(command);

        // Parse the response body
        const responseBody = JSON.parse(Buffer.from(response.body).toString());
        return responseBody;

    } catch (err) {
        console.error("Error invoking Claude 3 model:", err);
    }
}

// Invoke the function
const result = await invokeClaude3Haiku("what is ebs in aws");

console.log(result["content"][0]["text"]);
console.log(result);

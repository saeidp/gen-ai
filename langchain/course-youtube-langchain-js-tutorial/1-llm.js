// import { ChatOpenAI } from "@langchain/openai";

// const model = new ChatOpenAI({ 
//     openAIApiKey: ""
//  });

//  const response = await model.invoke("Hello")
//  console.log(response);

import { ChatBedrockConverse } from "@langchain/aws";

const llm = new ChatBedrockConverse({
    model: "anthropic.claude-3-haiku-20240307-v1:0",
    region: "ap-southeast-2",
    maxTokens: 300,
    temperature: 0.1,
    topP: 0.9
    // region: process.env.BEDROCK_AWS_REGION,
    // credentials: {
    //   accessKeyId: process.env.BEDROCK_AWS_ACCESS_KEY_ID!,
    //   secretAccessKey: process.env.BEDROCK_AWS_SECRET_ACCESS_KEY!,
    // },
});

const response = await llm.invoke(["Hello"])
console.log(response);
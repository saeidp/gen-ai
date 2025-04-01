import { ChatBedrockConverse } from "@langchain/aws";
// import { BaseMessage } from '@langchain/core/messages';
// import { trimMessages } from '@langchain/core/messages';
import { ChatPromptTemplate } from "@langchain/core/prompts";

const model = new ChatBedrockConverse({
    model: "anthropic.claude-3-haiku-20240307-v1:0",
    region: "ap-southeast-2",
    maxTokens: 300,
    temperature: 0.7,
});

// const prompt = ChatPromptTemplate.fromTemplate("You are a comedian, Tell a Joke based on the following word {input}");
// console.log(await prompt.format({ input: "chicken" }));
// const chain = prompt.pipe(model);
// const response = await chain.invoke({ input: "chicken" });
// console.log(response);

const prompt = ChatPromptTemplate.fromMessages([
    { role: "system", content: "You are a comedian, Tell a Joke based on a word provided by user"},
    { role: "human", content: "{input}" },
])

const chain = prompt.pipe(model);
const response = await chain.invoke({ input: "dog" });
console.log(response);
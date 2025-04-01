import { ChatBedrockConverse } from "@langchain/aws";
import { ChatPromptTemplate } from "@langchain/core/prompts";


const llm = new ChatBedrockConverse({
    model: "anthropic.claude-3-haiku-20240307-v1:0",
    region: "ap-southeast-2",
    maxTokens: 300,
    temperature: 0.7,
});

// A string holding the phrasing of the prompt
const standaloneQuestionTemplate = 'Given a question, convert it to a standalone question. question: {question} standalone question:'

// A prompt created using PromptTemplate and the fromTemplate method
const standaloneQuestionPrompt = ChatPromptTemplate.fromTemplate(standaloneQuestionTemplate)

// Take the standaloneQuestionPrompt and PIPE the model
const standaloneQuestionChain = standaloneQuestionPrompt.pipe(llm)

// Await the response when you INVOKE the chain. 
// Remember to pass in a question.
const response = await standaloneQuestionChain.invoke({
    question: 'What are the technical requirements for running Scrimba? I only have a very old laptop which is not that powerful.'
})

console.log(response)

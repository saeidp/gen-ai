import 'dotenv/config'; // Automatically loads .env variables

import { ChatBedrockConverse } from "@langchain/aws";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers"
import { RunnableSequence, RunnablePassthrough } from '@langchain/core/runnables';
import { combineDocuments } from './utils/combineDocuments.js';
import { retriever } from './utils/retriever.js';
import {formatConvHistory  } from './utils/formatConvHistory.js'


const llm = new ChatBedrockConverse({
    model: "anthropic.claude-3-haiku-20240307-v1:0",
    region: "ap-southeast-2",
    maxTokens: 300,
    temperature: 0.7,
});


const standaloneQuestionTemplate = `Given some conversation history (if any) and a question, convert the question to a standalone question. 
conversation history: {conv_history}
question: {question} 
standalone question:`
const standaloneQuestionPrompt = ChatPromptTemplate.fromTemplate(standaloneQuestionTemplate)

const answerTemplate = `You are a helpful and enthusiastic support bot who can answer a given question about Scrimba based on the context provided and the conversation history. Try to find the answer in the context. If the answer is not given in the context, find the answer in the conversation history if possible. If you really don't know the answer, say "I'm sorry, I don't know the answer to that." And direct the questioner to email help@scrimba.com. Don't try to make up an answer. Always speak as if you were chatting to a friend.
context: {context}
conversation history: {conv_history}
question: {question}
answer: `
 const answerPrompt = ChatPromptTemplate.fromTemplate(answerTemplate)
 

// const standaloneChain = standaloneQuestionPrompt.pipe(llm).pipe(new StringOutputParser());
 const standaloneQuestionChain = RunnableSequence.from([
    standaloneQuestionPrompt,
    llm,
    new StringOutputParser()
])

const retrieverChain = RunnableSequence.from([
    prevResult => prevResult.standalone_question,
    retriever,
    combineDocuments
])

// const answereChain = answerPrompt.pipe(llm).pipe(new StringOutputParser());
const answereChain = RunnableSequence.from([
    answerPrompt,
    llm,
    new StringOutputParser()
]);


 const chain = RunnableSequence.from([
    {
        standalone_question: standaloneQuestionChain,
        original_input: new RunnablePassthrough()
    },
    {
        context: retrieverChain,
        // question: ({original_input}) => original_input.question
        question: (prevResult) => prevResult.original_input.question,
        conv_history: ({ original_input }) => original_input.conv_history
    },
    answereChain
     
 ])

 const convHistory = []
 


 const question1= `my name is Saeid. What is Scrimba`
 const response1 = await chain.invoke({
    question: question1,
    conv_history: formatConvHistory(convHistory)
})
convHistory.push(question1)
convHistory.push(response1)

console.log("First Response: ", response1)
console.log("\n")


const question2= `What is my name?`
const response2 = await chain.invoke({
   question: question2,
   conv_history: formatConvHistory(convHistory)
})
convHistory.push(question2)
convHistory.push(response2)

console.log("Second Response: ", response2)


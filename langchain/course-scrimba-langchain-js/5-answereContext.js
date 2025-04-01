import 'dotenv/config'; // Automatically loads .env variables

import { ChatBedrockConverse } from "@langchain/aws";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers"
import { RunnableSequence, RunnablePassthrough } from '@langchain/core/runnables';
import { combineDocuments } from './utils/combineDocuments.js';
import { retriever } from './utils/retriever.js';


const llm = new ChatBedrockConverse({
    model: "anthropic.claude-3-haiku-20240307-v1:0",
    region: "ap-southeast-2",
    maxTokens: 300,
    temperature: 0.7,
});


const standaloneQuestionTemplate = `Given a question, convert it to a standalone question.
 question: {question}
 standalone question:`
 const standaloneQuestionPrompt = ChatPromptTemplate.fromTemplate(standaloneQuestionTemplate)

 const answerTemplate = `You are a helpful and enthusiastic support bot who can answer a given question about Scrimba based on the context provided. Try to find the answer in the context. If you really don't know the answer, say "I'm sorry, I don't know the answer to that." And direct the questioner to email help@scrimba.com. Don't try to make up an answer. Always speak as if you were chatting to a friend.
 context: {context}
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
        question: (prevResult) => prevResult.original_input.question
        // question: ({original_input}) => original_input.question
    },
    answereChain
     
 ])

// Returns all diocuments related to the standalone question
const response = await chain.invoke({
    question: `What are the technical requirements for running Scrimba? 
    I only have a very old laptop which is not that powerful.`
})
console.log(response)


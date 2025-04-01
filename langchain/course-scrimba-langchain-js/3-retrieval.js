import 'dotenv/config'; // Automatically loads .env variables

import { ChatBedrockConverse } from "@langchain/aws";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { BedrockEmbeddings } from "@langchain/aws";
import { SupabaseVectorStore } from "@langchain/community/vectorstores/supabase";
import { createClient } from "@supabase/supabase-js";
import { StringOutputParser } from "@langchain/core/output_parsers"


const sbApiKey = process.env.SUPABASE_API_KEY
const sbUrl = process.env.SUPABASE_URL


const llm = new ChatBedrockConverse({
    model: "anthropic.claude-3-haiku-20240307-v1:0",
    region: "ap-southeast-2",
    maxTokens: 300,
    temperature: 0.7,
});

const embeddings = new BedrockEmbeddings({
    model: "amazon.titan-embed-image-v1" ,
    region: "ap-southeast-2",
});

const client = createClient(sbUrl, sbApiKey)
const vectorStore = new SupabaseVectorStore(embeddings, {
    client,
    tableName: 'documents',
    queryName: 'match_documents'
})
const retriever = vectorStore.asRetriever()
// test the retriever
// const response2 = await retriever.invoke('Will Scrimba work on an old laptop?')
// console.log(response2)


const standaloneQuestionTemplate = `Given a question, convert it to a standalone question.
 question: {question}
 standalone question:`

 const standaloneQuestionPrompt = ChatPromptTemplate.fromTemplate(standaloneQuestionTemplate)
 
 // test the output parser
//  const standaloneQuestionChainWithparser = standaloneQuestionPrompt.pipe(llm).pipe(new StringOutputParser())
//  const response2 = await standaloneQuestionChainWithparser.invoke({
//     question: `What are the technical requirements for running Scrimba? 
//     I only have a very old laptop which is not that powerful.`
// })
// console.log(response2) 


// you need to extract the text (content) and send it to the retriever
 const chain = standaloneQuestionPrompt.pipe(llm).pipe(new StringOutputParser())
.pipe(retriever)

// Returns all diocuments related to the standalone question
const response = await chain.invoke({
    question: `What are the technical requirements for running Scrimba? 
    I only have a very old laptop which is not that powerful.`
})
console.log(response)


import { ChatBedrockConverse } from "@langchain/aws";
import { BedrockEmbeddings } from "@langchain/aws";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import {createStuffDocumentsChain} from "langchain/chains/combine_documents"
import { Document } from "langchain/document";
import { CheerioWebBaseLoader } from "@langchain/community/document_loaders/web/cheerio";
import {RecursiveCharacterTextSplitter } from 'langchain/text_splitter'
import {MemoryVectorStore} from 'langchain/vectorstores/memory'
import { createRetrievalChain } from "langchain/chains/retrieval";
const model = new ChatBedrockConverse({
    model: "anthropic.claude-3-haiku-20240307-v1:0",
    region: "ap-southeast-2",
    maxTokens: 300,
    temperature: 0.7,
});

//----------------------create document chain-----------------------------------------------------
//// Information from the website
// const prompt = ChatPromptTemplate.fromTemplate(`
//     Answere the user's question.
//     context: {context}
//     {input}
// `);
// const chain = await createStuffDocumentsChain({
//     llm: model,
//     prompt:prompt
// })

// const documentA = new Document({
//     pageContent: "The LangChain Expression Language (LCEL) takes a declarative approach to building new Runnables from existing Runnables.",
//     // metadata: { source: "https://en.wikipedia.org/wiki/Langchain_(framework)" },
// })

// const response = await chain.invoke({
//     input: "What is LCEL?",
//     context: [documentA]
// });

// console.log(response);

// ----------------------------------Loader---------------------------
// // Information from the website using cheerio
const prompt = ChatPromptTemplate.fromTemplate(`
    Answere the user's question.
    context: {context}
    Question:{input}
`);
const chain = await createStuffDocumentsChain({
    llm: model,
    prompt:prompt
})

const loader = new CheerioWebBaseLoader("https://js.langchain.com/docs/how_to/#langchain-expression-language-lcel")
const docs = await loader.load()
// console.log(docs)

// feeding all the page content is expensive as this page has 15708 characters
console.log(docs[0].pageContent.length)

const response = await chain.invoke({
    input: "What is LCEL?",
    context: docs
});
console.log(response);

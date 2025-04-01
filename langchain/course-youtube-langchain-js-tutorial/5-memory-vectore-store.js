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

// -------------------------------Splitter and memory vector store-------------------------------------------
// this is not working due to issue in embedding. It might be of issue with the model cohere

//  Splitter can save us the character from the website
const prompt = ChatPromptTemplate.fromTemplate(`
    Answere the user's question.
    Context: {context}
    Question: {input}`
);
const documentChain = await createStuffDocumentsChain({
    llm: model,
    prompt:prompt
})

const loader = new CheerioWebBaseLoader("https://js.langchain.com/docs/how_to/#langchain-expression-language-lcel")
const docs = await loader.load()

const splitter = new RecursiveCharacterTextSplitter({
    // separators: ["\n\n", "\n", " ", ""],
    chunkSize: 200, 
    chunkOverlap: 20
})

const splitDocs = await splitter.splitDocuments(docs)
// console.log(splitDocs)

const embeddings = new BedrockEmbeddings({
    model: "amazon.titan-embed-image-v1" ,
    region: "ap-southeast-2",
});

// Only a test to see if embedding works
//-----------------------start of test-------------------------
// const res = await embeddings.embedQuery(
//     "What would be a good company name for a company that makes colorful socks?"
//   );
//   console.log(res)

// const text = "What is LCEL?"
// const vectorstore = await MemoryVectorStore.fromDocuments(
//     [{ pageContent: text, metadata: {} }],
//     embeddings
//   );
//---------------- end of test ------------------------

const vectorstore = await MemoryVectorStore.fromDocuments(splitDocs, embeddings);

const retriever = vectorstore.asRetriever({
    k: 2 //default 3
})

const retrievalChain = await createRetrievalChain( {retriever, combineDocsChain: documentChain})

// it does not need contecxt: docs as it automatically fetch the relevant docs
const response = await retrievalChain.invoke({
    input: "What is LCEL?" // this input is the name defined above. don't change that
});
console.log(response);
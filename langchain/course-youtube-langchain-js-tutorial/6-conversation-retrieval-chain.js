import { ChatBedrockConverse } from "@langchain/aws";
import { BedrockEmbeddings } from "@langchain/aws";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { CheerioWebBaseLoader } from "@langchain/community/document_loaders/web/cheerio";
import {RecursiveCharacterTextSplitter } from 'langchain/text_splitter'
import {MemoryVectorStore} from 'langchain/vectorstores/memory'
import { createRetrievalChain } from "langchain/chains/retrieval";
import { createHistoryAwareRetriever } from "langchain/chains/history_aware_retriever";
import { MessagesPlaceholder } from "@langchain/core/prompts";
import { HumanMessage, AIMessage } from "@langchain/core/messages";
import { createStuffDocumentsChain } from "langchain/chains/combine_documents";



const createVectoreStore = async () => {
    // loader
    const loader = new CheerioWebBaseLoader("https://js.langchain.com/docs/how_to/#langchain-expression-language-lcel")
    const docs = await loader.load()

    // text splitter
    const splitter = new RecursiveCharacterTextSplitter({
        // separators: ["\n\n", "\n", " ", ""],
        chunkSize: 100, 
        chunkOverlap: 20
    })

    const splitDocs = await splitter.splitDocuments(docs)
    // console.log(splitDocs)

    // embeddings
    const embeddings = new BedrockEmbeddings({
        model: "amazon.titan-embed-image-v1" ,
        region: "ap-southeast-2",
    });

    // create vector store
    const vectorstore = await MemoryVectorStore.fromDocuments(splitDocs, embeddings);
    return vectorstore
    
}

const createConversationalRetrievalChain = async (vectorStore) => {
    const model = new ChatBedrockConverse({
        model: "anthropic.claude-3-haiku-20240307-v1:0",
        region: "ap-southeast-2",
        maxTokens: 300,
        temperature: 0.7,
    });
    // this retriever is not aware of history
    const retriever = vectorStore.asRetriever({
        k: 2 //default 3
    })
    
    // Create a HistoryAwareRetriever which will be responsible for
    // generating a search query based on both the user input and
    // the chat history
    // in documentation two user input is used but it generates error
    // if if not using assistant. I created the assistant based on chatgpt suggestion
    const historyAwarePrompt = ChatPromptTemplate.fromMessages([
        new MessagesPlaceholder("chat_history"),
        ["user", "{input}"],
        [
          "assistant",
          "I will generate a search query based on the above conversation. Please wait...",
        ], // Assistant message before generating the query
        [
          "user",
          "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation",
        ],
      ]);
      
      // console.log(historyAwarePrompt)

    // This chain will return a list of documents from the vector store
    const historyAwareRetrieverChain   = await createHistoryAwareRetriever({
        llm: model,
        retriever,
        rephrasePrompt: historyAwarePrompt,
      });
    
      // ---------just for test
      //This trace illustrates that this returns documents about LCEL. 
      //This is because the LLM generated a new query, combining the chat history
      // with the follow up question.
      // const chatHistory = [
      // new HumanMessage("What does LCEL stand for?"),
      // new AIMessage("LangChain Expression Language"),
      // ];
      // await historyAwareRetrieverChain.invoke({
      //   chat_history: chatHistory,
      //   input: "What is it?",
      // });
      //-----------
     
    const historyAwareRetrievalPrompt = ChatPromptTemplate.fromMessages([
        [
          "system",
          "Answer the user's questions based on the following context: {context}.",
        ],
        new MessagesPlaceholder("chat_history"),
        ["user", "{input}"],
      ]);
    
    // Since we need to pass the docs from the retriever, we will use
    // the createStuffDocumentsChain
    const historyAwareCombineDocsChain = await createStuffDocumentsChain({
        llm: model,
        prompt: historyAwareRetrievalPrompt,
      });
    
    // Create the conversation chain, which will combine the retrieverChain
    // and combineStuffChain in order to get an answer
    const conversationalRetrievalChain  = await createRetrievalChain({
      retriever: historyAwareRetrieverChain,
      combineDocsChain: historyAwareCombineDocsChain
      });
    
    return conversationalRetrievalChain     

}

const vectorStore = await createVectoreStore()
const conversationalRetrievalChain = await createConversationalRetrievalChain(vectorStore)

 // Fake chat history
 const chatHistory = [
    new HumanMessage("What does LCEL stand for?"),
    new AIMessage("LangChain Expression Language"),
  ];


  // Test: you pass what is it but because it has history it returns correct values
const response = await conversationalRetrievalChain.invoke({
    chat_history: chatHistory,
    input: "What is it?",
  });
  console.log(response.answer);
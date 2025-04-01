import { RunnableSequence } from "@langchain/core/runnables";
import { ChatBedrockConverse } from "@langchain/aws";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers"



const punctuationTemplate = `Given a sentence, add punctuation where needed. please don't fix the grammar only punctuation.  
    sentence: {sentence}
    sentence with punctuation:  
    `
const punctuationPrompt = ChatPromptTemplate.fromTemplate(punctuationTemplate)

const grammarTemplate = `Given a sentence correct the grammar.
    sentence: {punctuated_sentence}
    sentence with correct grammar: 
    `
const grammarPrompt = ChatPromptTemplate.fromTemplate(grammarTemplate)


const llm = new ChatBedrockConverse({
    model: "anthropic.claude-3-haiku-20240307-v1:0",
    region: "ap-southeast-2",
    maxTokens: 300,
    temperature: 0.7,
});

const chain = RunnableSequence.from([
    // prevResult => console.log(prevResult),
    // output: { sentence: 'i dont liked mondays', language: 'french' }
    punctuationPrompt,
    llm,
    //prevResult => console.log(prevResult),

    new StringOutputParser(),
    // prevResult => console.log(prevResult),
    // output: idon't liked Mondays.

])
// I don't liked Mondays. It shows that grammar is not yet fixed
const response = await chain.invoke({
    sentence: 'i dont liked mondays',
    language: 'french'
})

console.log(response)
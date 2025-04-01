import { RunnableSequence, RunnablePassthrough } from "@langchain/core/runnables";
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

// we need to pass language as we need it in chain we need runnable pass through
const translationTemplate = `Given a sentence, translate that sentence into {language}
    sentence: {grammatically_correct_sentence}
    translated sentence:
    `
const translationPrompt = ChatPromptTemplate.fromTemplate(translationTemplate)



const llm = new ChatBedrockConverse({
    model: "anthropic.claude-3-haiku-20240307-v1:0",
    region: "ap-southeast-2",
    maxTokens: 300,
    temperature: 0.7,
});

const punctuationChain = RunnableSequence.from([
    punctuationPrompt,
     llm,
     new StringOutputParser()])

const grammerChain = RunnableSequence.from([
    grammarPrompt,
    llm, 
    new StringOutputParser()])

const translationChain = RunnableSequence.from([
    translationPrompt, 
    llm, 
    new StringOutputParser()])

const chain =RunnableSequence.from([
    {
        punctuated_sentence: punctuationChain,
        original_input: new RunnablePassthrough()

    },
    {
        grammatically_correct_sentence: grammerChain,
        language: (prevResult) => prevResult.original_input.language
        //or
        // language: ({ original_input }) => original_input.language
    },
    translationChain
])


// I don't liked Mondays. It shows that grammar is not yet fixed
const response = await chain.invoke({
    sentence: 'i dont liked mondays',
    language: 'french'
})

console.log(response)
// output: I don't like Mondays.
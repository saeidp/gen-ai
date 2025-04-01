import { ChatBedrockConverse } from "@langchain/aws";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser, CommaSeparatedListOutputParser, StructuredOutputParser } from "@langchain/core/output_parsers";
import { z } from "zod";

const model = new ChatBedrockConverse({
    model: "anthropic.claude-3-haiku-20240307-v1:0",
    region: "ap-southeast-2",
    maxTokens: 300,
    temperature: 0.7,
});

async function callStringOutputParser() {
    const prompt = ChatPromptTemplate.fromMessages([
        { role: "system", content: "Generate a Joke based on a word provided by the user"},
        { role: "human", content: "{input}" },
    ])
    const parser = new StringOutputParser();
    const chain = prompt.pipe(model).pipe(parser);
    return await chain.invoke({ input: "dog" });
}

async function callListOutputParser() {
    const prompt = ChatPromptTemplate.fromTemplate("Provide 5 synonyms, separated by commas, for the following word {word}");
    const outputParser = new CommaSeparatedListOutputParser();
    const chain = prompt.pipe(model).pipe(outputParser);
    return await chain.invoke({ word: "happy" });
}

async function callStructuredOutputParser() {
    const prompt = ChatPromptTemplate.fromTemplate(`Extract information from the following phrases.
          Formatting Instructions: {format_instructions}
          Phrases: {phrases}`);

    const outputParser = StructuredOutputParser.fromNamesAndDescriptions({
        name: "the name of the person",
        age: "The age of the person",
    });
    const chain = prompt.pipe(model).pipe(outputParser);
    return await chain.invoke({ 
        phrases: "Max is 30 years old.",
        format_instructions:outputParser.getFormatInstructions()
        // format_instructions: {name: "the name of the person", age: "The age of the person"},

   });
}

async function callZodOutputParser() {
    const prompt = ChatPromptTemplate.fromTemplate(`Extract information from the following phrases.
          Formatting Instructions: {format_instructions}
          Phrases: {phrases}`);
    
    const schema = z.object({
        name: z.string().describe("the name of the person"),
        age: z.number().describe("The age of the person"),
    });

     // Wrap the Zod schema with LangChain's StructuredOutputParser
    const outputParser = StructuredOutputParser.fromZodSchema(schema);

    const chain = prompt.pipe(model).pipe(outputParser);
    return await chain.invoke({ 
        phrases: "Max is 30 years old.",
        format_instructions:outputParser.getFormatInstructions()

   });
}

// const response = await callStringOutputParser();
// console.log(response);

// const response = await callListOutputParser();
// console.log(response);

// const response = await callStructuredOutputParser();
// console.log(response);

const response = await callZodOutputParser();
console.log(response);

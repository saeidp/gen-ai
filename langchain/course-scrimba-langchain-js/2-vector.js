import 'dotenv/config'; // Automatically loads .env variables

import { BedrockEmbeddings } from "@langchain/aws";
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter'
import { SupabaseVectorStore } from "@langchain/community/vectorstores/supabase";
import { createClient } from "@supabase/supabase-js";
import { readFile } from 'fs/promises';

// @supabase/supabase-js
try {
    // dimention is 1024
    const embeddings = new BedrockEmbeddings({
        model: "amazon.titan-embed-image-v1" ,
        region: "ap-southeast-2",
    });

    const text = await readFile('./scrimba-info.txt', 'utf8'); // Read local file
    const splitter = new RecursiveCharacterTextSplitter({
        chunkSize: 500,
        chunkOverlap: 50,
        separators: ['\n\n', '\n', ' ', ''] // default setting
    })
    
    const output = await splitter.createDocuments([text])
    
    const sbApiKey = process.env.SUPABASE_API_KEY
    const sbUrl = process.env.SUPABASE_URL

    const client = createClient(sbUrl, sbApiKey)

    await SupabaseVectorStore.fromDocuments(
        output,
        embeddings,
        {
           client,
           tableName: 'documents',
        }
    )
    
} catch (err) {
    console.log(err)
}






// const supabaseUrl = process.env.SUPABASE_URL;
// const supabaseApiKey = process.env.SUPABASE_API_KEY;

// console.log("Supabase URL:", supabaseUrl);
// console.log("Supabase API Key:", supabaseApiKey ? "Loaded" : "Missing");


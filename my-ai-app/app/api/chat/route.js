import { createGoogleGenerativeAI } from '@ai-sdk/google';
import { streamText, convertToCoreMessages } from 'ai';
const google = createGoogleGenerativeAI({
  apiKey: "AIzaSyCBZCn2VZT224OtUKvT Ll3F6osGF1M5rng",
});

const SERP_API_KEY = '3dd2b48eef6e177d9d2c51cdf3c1e11b813818da6b3ed09fecf8b7c7bba8cf4f'; 

export const maxDuration = 30;

export async function POST(req) {
  try {
    const { messages } = await req.json();
    const userQuery = messages[messages.length - 1].content; 
    console.log("User Query:", userQuery);
    const serpApiResponse = await fetch(`https://serpapi.com/search.json?q=${encodeURIComponent(userQuery)}&api_key=${SERP_API_KEY}`);
    const serpData = await serpApiResponse.json();
    let serpInfo = '';
    if (serpData && serpData.organic_results) {
      serpInfo = await serpData.organic_results
        .filter(result => result.snippet && (result.snippet.includes('stock') || result.snippet.includes('financial')))
        .map(result => result.snippet)
        .join('\n');
    } else {
      serpInfo = 'No relevant information found.';
    }
    console.log("Filtered SERP API Info:", serpInfo);
    const systemInstruction =`
      You are a financial analyst with expertise in global financial markets, including stocks and trends.
      Analyze the following stock-related information,
      ${serpInfo}
      just print the information i have provided in a short and clear manner and please dont give any source to other links or pages and dont give any suggestions
    `;
    console.log("System Instruction:", systemInstruction); 
const message=userQuery;
    const result = await streamText({
      model: google('gemini-1.5-flash-latest'),
      
      messages: [
        { role: 'user', content: systemInstruction }]
    });
    return result.toDataStreamResponse();
  } catch (error) {
    console.error('Error occurred:', error);
    return new Response(`Error: ${error.message}`, { status: 500 });
  }
}

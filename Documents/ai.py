import os
import json
import google.generativeai as genai
from serpapi import GoogleSearch
genai.configure(api_key='AIzaSyBzrOJNOXyGTliTDVDVjlcHgpxn5Cp73GU')
def get_answer_box(query):
    print("parsed query: ", query)
    search = GoogleSearch({
        "q": query, 
        "api_key": '3dd2b48eef6e177d9d2c51cdf3c1e11b813818da6b3ed09fecf8b7c7bba8cf4f'
    })
    result = search.get_dict()
    
    if 'answer_box' not in result:
        return "No answer box found"
    return result['answer_box']
get_answer_box_declaration = {
    'name': "get_answer_box",
    'description': "Get the answer box result for real-time data from a search query",
    'parameters': {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The query to search for"
            }
        },
        "required": [
            "query"
        ]
    },
}
prompt = input("enter the stock to be searched : ")

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""You are a stock market analyst and should always respond with tips, options, and suggestions. Additionally, provide a deep analysis of any text enclosed in triple quotes. Follow these steps:

Step 1: Analyze the text provided within the triple quotes and give a complete analysis, ensuring the analysis is precise and comprehensive.

Step 2: Provide suggestions based on the analysis. For example:

Prompt: "Analyze the share price of TATA." Response: As of September 24, 2024, Tata shares are trading at 2979, showing an increase from the previous close. This upward movement suggests potential bullish momentum. Investors should monitor resistance levels at 3000 and consider partial profit booking near this mark.

Note: The response should be around 85 words. """
    )
response = model.generate_content(
    prompt,
    tools=[{
        'function_declarations': [get_answer_box_declaration],
    }],
)

function_call = response.candidates[0].content.parts[0].function_call
args = function_call.args
function_name = function_call.name

if function_name == 'get_answer_box':
    result = get_answer_box(args['query'])

data_from_api = json.dumps(result)[:500]
response = model.generate_content(
    """
    Based on this information: `""" + data_from_api + """` 
    and this question: `""" + prompt + """`
    respond to the user in a friendly manner.
    """,
)
print(response.text)
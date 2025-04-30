from openai import OpenAI

def extract_data(final_output, cleaned_text, all_links_list, openai_api_key, llm_model):
    try:  
        client = OpenAI(
            base_url = "https://openrouter.ai/api/v1",
            api_key = openai_api_key,
        ) 

        prompt = f"""
        You are an intelligent data extraction assistant.

        Your task is:
        1. Update the previously found fields if better information is found.
        2. Extract any missing fields from the current page if available.
        3. Suggest which link(s) from the page are most likely to help find the missing details.

        Inputs:
        Previously found data (may be incomplete):
        {final_output}

        All links on current page:
        {all_links_list}

        Current webpage content:
        {cleaned_text}

        Instructions:
        - check the webpage text for missing details.
        - If better information is found for already extracted fields, only then update it.
        - Do not guess or hallucinate information; only use what is explicitly available.
        - Preserve already found fields unless better information is found. Output relevant data.
        - After processing, return three parts:
        1. "found" — with already found, updated and newly found correct fields as key-value pairs
        2. "missing" — list of field names still missing
        3. "suggested_links" — 2-3 best URLs (from the given list) likely to help find the missing fields, also arrange the links in priority order, starting with the link on which the chances are highest to find the missing data and ending at the link with least possibility of having the missing data available

        Output format:

        {{
        "found": {{
            "field1": "value1",
            "field2": "value2",
            ...
        }},
        "missing": ["fieldX", "fieldY", ...],
        "suggested_links": ["link1", "link2", ...]
        }}
        """

        response = client.chat.completions.create(
            model= llm_model, #"deepseek/deepseek-chat-v3-0324", #"mistralai/mistral-tiny", #"deepseek/deepseek-chat-v3-0324:free", #"gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in OpenAI extraction: {e}")
        return None

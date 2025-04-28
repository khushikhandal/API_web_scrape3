from openai import OpenAI

def extract_data(data_needed, cleaned_text, all_links_list, social_links, emails, phone_nos, openai_api_key):
    try:  
        client = OpenAI(
            base_url = "https://openrouter.ai/api/v1",
            api_key = openai_api_key,
        ) 

        prompt = f"""
        You are an intelligent data extraction assistant.

        Your task is to:
        1. Extract the following details: {data_needed}
        2. First search in the structured data like emails, phone numbers, and social media links.
        3. Then, search the unstructured webpage content to extract any remaining details.
        4. At the end, suggest which link(s) from the page are most likely to help find the missing details.

        Inputs:

        Structured data:
        - Emails found (if any): {emails}
        - Phone numbers found (if any): {phone_nos}
        - Social media links (if any): {social_links}

        All links on page:
        {all_links_list}

        Webpages' content:
        {cleaned_text}

        Instructions:
        - Use structured data first.
        - Then scan the webpage text to extract remaining values.
        - Use only what is explicitly available; do not guess.
        - Return two sections:
        1. "found" — with the fields you successfully extracted, as JSON key:value pairs
        2. "missing" — a list of field names that were not found
        3. "suggested_links" — URLs (from the given list) likely to contain the missing fields

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
        model="gpt-4-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=0
        )

        return (response.choices[0].message.content)
    except Exception as e:
        print ("Error in Openai code: ", e)
        return None
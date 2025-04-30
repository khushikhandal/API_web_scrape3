from bs_operations import *
from extract_by_openai import extract_data
from getpage_zyte import getpage
import json
import tiktoken

def count_tokens(text, model="gpt-4-turbo"):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

def web_scrape(url, final_output, zyte_api_key, openai_api_key, llm_model):
    html_page = getpage(url,zyte_api_key)
    #for zyte
    if (html_page != None):
        parse_all_data(html_page)

        cleaned_text = clean_text()
        all_links_list = list(set(all_href_links()))

        print("tokens: ", count_tokens(cleaned_text))
        output = extract_data(final_output, cleaned_text, all_links_list, openai_api_key, llm_model)
        #print("output",output)
        #for openai
        if(output != None):
            try:
                clean_output = output.replace("```json", "").replace("```", "").strip()
                output_dict = json.loads(clean_output)
                return output_dict
            except Exception as e:
                print("json error : ",e)
                #print(clean_output)
                return None
        else:
            return None
    else:
        return None
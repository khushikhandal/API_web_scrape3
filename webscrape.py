from bs_operations import *
from extract_by_openai import extract_data
from getpage_zyte import getpage
import json

#count tokens
import tiktoken
def count_tokens(text, model="gpt-4-turbo"):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

def web_scrape(url, data_needed, zyte_api_key, openai_api_key):
    html_page = getpage(url,zyte_api_key)

    #For zyte's output
    if (html_page != None):
        parse_all_data(html_page)

        cleaned_text = clean_text()
        all_links_list = list(set(all_href_links()))
        social_links = list(set(social_media_links()))
        emails = list(set(get_emails()))
        phone_nos = list(set(get_phone_nos()))

        #print tokens
        print("tokens: ", count_tokens(cleaned_text))

        output = extract_data(data_needed, cleaned_text, all_links_list, social_links, emails, phone_nos, openai_api_key)
        #print("output",output)
        #For openai's output
        if(output != None):
            clean_output = output.replace("```json", "").replace("```", "").strip()
            output_dict = json.loads(clean_output)
            return output_dict
        else:
            return None
    else:
        return None
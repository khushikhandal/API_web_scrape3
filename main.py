#uvicorn main:app --reload
#http://127.0.0.1:8000/docs

from fastapi import FastAPI
from pydantic import BaseModel
from webscrape import web_scrape
from typing import Optional

app = FastAPI()

class RequestData(BaseModel):
    url: str
    data_needed: str
    runs: Optional[int] = 1
    llm_model: Optional[str]="deepseek/deepseek-chat-v3-0324"
    zyte_api_key: str
    openai_api_key: str

@app.post("/web_scrape")
def ping(data: RequestData):
    url = data.url
    data_needed = data.data_needed
    runs = data.runs
    llm_model= data.llm_model
    zyte_api_key = data.zyte_api_key
    openai_api_key = data.openai_api_key

    runs = max(1, min(runs, 20))

    url_list = url.split(",") #list
    needed_data = data_needed.split(",") #string
    final_output = {'found':{}, 'missing':needed_data, 'suggested_links':url_list} #dictionary

    i=0
    while(i<runs): 
        if(needed_data != [] and needed_data != None):
            #print("url being scrape: ", url_list[i])
            #print("url list right now: ",url_list)
            output = web_scrape(url_list[i], final_output, zyte_api_key, openai_api_key, llm_model)
            #print("output: ",output)
            i = i+1
            if (output != None and output["missing"] != None and output["missing"]!=[]):
                final_output.update(output)
                url_list.extend(output["suggested_links"])
            else:
                if(output!= None):
                    final_output.update(output)
                    break
                else:
                    continue      
        else:
            break

    #print(final_output)
    return final_output
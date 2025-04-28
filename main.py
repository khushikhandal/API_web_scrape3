#uvicorn main:app --reload
#http://127.0.0.1:8000/docs

from fastapi import FastAPI
from pydantic import BaseModel
from webscrape import web_scrape
from typing import Optional

app = FastAPI()

# Request model
class RequestData(BaseModel):
    url: str
    data_needed: str
    runs: Optional[int] = 1
    zyte_api_key: str
    openai_api_key: str

@app.post("/web_scrape")
def ping(data: RequestData):
    url = data.url
    data_needed = data.data_needed
    runs = data.runs
    zyte_api_key = data.zyte_api_key
    openai_api_key = data.openai_api_key

    if (runs < 1):
        runs = 1
    if (runs > 10):
        runs = 10

    url_list = url.split(",") #list
    needed_data = data_needed #string
    final_output = {'found':{}, 'missing':[], 'suggested_links':[]} #dictionary

    i=0
    while(i<runs):
        if((needed_data.strip() != '')):
            output = web_scrape(url_list[i], needed_data, zyte_api_key, openai_api_key)

            if (output != None):
                final_output['found'].update(output['found'])
                needed_data = ",".join(output["missing"])
                url_list.extend(output["suggested_links"])
        else:
            break
        i = i+1

    final_output["missing"] = output["missing"]
    final_output["suggested_links"] = list(set(url_list[runs:]))

    return final_output
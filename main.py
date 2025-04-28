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
    zyte_api_key: str
    openai_api_key: str

@app.post("/web_scrape")
def ping(data: RequestData):
    url = data.url
    data_needed = data.data_needed
    runs = data.runs
    zyte_api_key = data.zyte_api_key
    openai_api_key = data.openai_api_key

    runs = max(1, min(runs, 20))

    url_list = url.split(",") #list
    needed_data = data_needed.split(",") #string
    final_output = {'found':{}, 'missing':needed_data, 'suggested_links':url_list} #dictionary

    i=0
    while(i<runs):
        if(needed_data != [] and needed_data != None):
            output = web_scrape(url_list[i], final_output, zyte_api_key, openai_api_key)

            if (output["missing"] != None and output["missing"]!=[]):
                final_output.update(output)
                url_list.extend(output["suggested_links"])
        else:
            break
        i = i+1

    print(final_output)
    return final_output
from zyte_api import ZyteAPI
import base64

#https://python-zyte-api.readthedocs.io/en/stable/
def getpage(url, zyte_api_key):
    try:
        client = ZyteAPI(api_key = zyte_api_key)
        response = client.get({"url": url, "httpResponseBody": True})
        html_base64 = response["httpResponseBody"]
        html = base64.b64decode(html_base64).decode("utf-8")
        return html
    except Exception as e:
        print ("Error in Zyte code: ", e, "for url: ", url)
        return None
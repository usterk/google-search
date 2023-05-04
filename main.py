import os
import time
from fastapi import FastAPI
from googleapiclient.discovery import build
import logging

app = FastAPI()

api_key = os.environ["GOOGLE_SEARCH_API"]
cse_id = os.environ["GOOGLE_CSE_ID"]
google_search_service = build("customsearch", "v1", developerKey=api_key)

def fetch_search_result_links(search_phrase):
    result_links = []
    retries = 1

    while retries >= 0:
        try:
            response = google_search_service.cse().list(q=search_phrase, cx=cse_id, num=3).execute()
            for item in response['items']:
                result_links.append(item['link'])
            break
        except Exception as e:
            print(f"Error during search: {e}")
            retries -= 1
            if retries >= 0:
                time.sleep(1)

    return result_links

@app.get("/google/{phrase}")
async def google(phrase: str):
    return {"results": fetch_search_result_links(phrase)}

@app.on_event("startup")
async def on_startup():
    logging.info("Application startup complete.")
    logging.info("Example API request with curl:")
    logging.info("curl http://localhost:3100/google/your_search_phrase")
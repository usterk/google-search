import os
from fastapi import FastAPI
from googleapiclient.discovery import build

app = FastAPI()

api_key = os.environ["GOOGLE_SEARCH_API"]
cse_id = os.environ["GOOGLE_CSE_ID"]
google_search_service = build("customsearch", "v1", developerKey=api_key)

def fetch_search_result_links(search_phrase):
    result_links = []
    try:
        response = google_search_service.cse().list(q=search_phrase, cx=cse_id, num=3).execute()
        for item in response['items']:
            result_links.append(item['link'])
    except Exception as e:
        print(f"Error during search: {e}")
    
    return result_links

@app.get("/google/{phrase}")
async def google(phrase: str):
    return {"results": fetch_search_result_links(phrase)}

@app.on_event("startup")
async def on_startup():
    print("Application startup complete.")
    print("Example API request with curl:")
    print("curl http://localhost:3100/google/your_search_phrase")
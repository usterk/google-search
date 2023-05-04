import os
from dotenv import load_dotenv
from fastapi import FastAPI
from googleapiclient.discovery import build

load_dotenv()  # Load the environment variables from the .env file

app = FastAPI()

api_key = os.getenv("GOOGLE_SEARCH_API")
google_search_service = build("customsearch", "v1", developerKey=api_key)

def pobierz_linki_wynikow(fraza_wyszukiwania):
    linki_wynikow = []
    try:
        response = google_search_service.cse().list(q=fraza_wyszukiwania, cx="017576662512468239146:omuauf_lfve", num=3).execute()
        for item in response['items']:
            linki_wynikow.append(item['link'])
    except Exception as e:
        print(f"Błąd podczas wyszukiwania: {e}")
    
    return linki_wynikow

@app.get("/google/{fraza}")
async def google(fraza: str):
    return {"wyniki": pobierz_linki_wynikow(fraza)}

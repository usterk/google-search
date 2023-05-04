from fastapi import FastAPI
from googlesearch import search

app = FastAPI()

def pobierz_linki_wynikow(fraza_wyszukiwania):
    linki_wynikow = []
    try:
        for link in search(fraza_wyszukiwania, num_results=3):
            linki_wynikow.append(link)
    except Exception as e:
        print(f"Błąd podczas wyszukiwania: {e}")
    
    return linki_wynikow

@app.get("/wyszukaj/{fraza}")
async def wyszukaj(fraza: str):
    return {"wyniki": pobierz_linki_wynikow(fraza)}

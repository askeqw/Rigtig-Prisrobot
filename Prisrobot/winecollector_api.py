import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://www.winecollector.dk/wp-json/wc/v3"
CK = os.getenv("ck_415122ee21ec03718f44f090ac8d0bf0f4f175a5")
CS = os.getenv("cs_fdc4810fb8072f4b3ac6f90a3ba6ce8e806bc073")

def hent_mest_solgte(limit=10):
    url = f"{BASE_URL}/products"
    params = {
        "orderby": "popularity",
        "per_page": limit,
        "status": "publish"
    }

    response = requests.get(url, auth=HTTPBasicAuth(CK, CS), params=params)

    if response.status_code != 200:
        print("❌ Fejl ved hentning:", response.status_code, response.text)
        return []

    produkter = response.json()

    vine = []
    for produkt in produkter:
        navn = produkt.get("name")
        pris = produkt.get("price")
        if navn and pris:
            vine.append({
                "navn": navn,
                "egen_pris": pris
            })

    return vine

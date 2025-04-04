import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Hent én nøgle og CSE-ID pr. konkurrent
CSE_CONFIG = {
    "finewines": {
        "key": os.getenv("AIzaSyAXzhTgwq5A7TO4pM31zxMcUyIdDh5czYo"),
        "cx": os.getenv("4535a3fb7213747f6")
    },
    "theisvine": {
        "key": os.getenv("AIzaSyAXEsGljjRmhciBZl2ESShuyeMS6MleERo"),
        "cx": os.getenv("97e1819ca22ec432c")
    },
    "densidsteflaske": {
        "key": os.getenv("AIzaSyBDVEMaz85DHL6RGD7cODgbatnOnUundBo"),
        "cx": os.getenv("84a9d5d294a8b4fe5")
    },
    "bottlehero": {
        "key": os.getenv("AIzaSyDxgf-xS0qori4s0tI59J4ODgbSPHLm-80"),
        "cx": os.getenv("a4e6be18cc8a94de4")
    },
}

# ✔️ Tjek for manglende værdier
for kilde, config in CSE_CONFIG.items():
    if not config["key"] or not config["cx"]:
        raise EnvironmentError(f"API-nøgle eller CSE-ID mangler for {kilde.upper()} i .env")

def find_links(vinnavn, kilde, max_results=2):
    config = CSE_CONFIG.get(kilde)
    if not config:
        raise ValueError(f"Ukendt kilde: {kilde}")

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": vinnavn,
        "key": config["key"],
        "cx": config["cx"],
        "num": max_results
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"[{kilde.upper()}] HTTP-fejl: {response.status_code} – {response.text}")
            return []

        data = response.json()
        return [item["link"] for item in data.get("items", [])]

    except requests.exceptions.RequestException as e:
        print(f"[{kilde.upper()}] Netværksfejl: {e}")
        return []

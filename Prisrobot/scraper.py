import requests
from bs4 import BeautifulSoup

def hent_pris_fra_url(url, kilde):
    try:
        # Filtrér irrelevante URL'er
        if not "/products/" in url:
            print(f"[{kilde.upper()}] Ignorerer ikke-produktlink: {url}")
            return None

        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        pris_element = None

        if kilde == "finewines":
            pris_element = soup.select_one(".price")

        elif kilde == "densidsteflaske":
            pris_element = (
                soup.select_one(".product__price span") or
                soup.select_one(".product__price") or
                soup.select_one(".product-price")
            )

        elif kilde == "theisvine":
            pris_element = (
                soup.select_one(".product__price span") or
                soup.select_one(".product__price") or
                soup.select_one(".product-price")
            )

        elif kilde == "bottlehero":
            pris_element = (
                soup.select_one("span.product-price") or
                soup.select_one(".price-item--regular") or
                soup.select_one(".product__price") or
                soup.select_one(".price")
            )

        else:
            print(f"[{kilde.upper()}] Ukendt kilde: {url}")
            return None

        if not pris_element:
            print(f"[{kilde.upper()}] Kunne ikke finde pris på siden: {url}")
            return None

        pris_tekst = pris_element.get_text(strip=True)

        # Hvis teksten ikke indeholder tal, er det næppe en pris
        if not any(char.isdigit() for char in pris_tekst):
            print(f"[{kilde.upper()}] Ingen tal i prisfeltet – springer over: '{pris_tekst}'")
            return None

        print(f"[{kilde.upper()}] Pris fundet: {pris_tekst}")

        pris = float(
            pris_tekst
                .replace("kr", "")
                .replace("DKK", "")
                .replace(".", "")      # Fjerner tusindtalsseparator
                .replace(",", ".")     # Gør klar til float
                .strip()
        )

        return pris

    except Exception as e:
        print(f"[{kilde.upper()}] Fejl ved scraping af {url}: {e}")
        return None

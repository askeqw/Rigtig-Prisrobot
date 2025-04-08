from cse import CSE_IDS, find_links
from scraper import hent_pris_fra_url

def sammenlign_med_konkurrenter(vine):
    resultat = []

    for vin in vine:
        navn = vin.get("navn")
        egen_pris = vin.get("egen_pris", "-")
        try:
            egen_pris_float = float(str(egen_pris).replace(",", "."))
        except:
            egen_pris_float = None

        vin_resultat = {
            "navn": navn,
            "egen_pris": egen_pris,
            "konkurrenter": {},
            "billigste": "os",  # Default til os selv
        }

        billigste_pris = egen_pris_float if egen_pris_float is not None else None
        billigste_kilde = "os"

        print(f"\n→ Behandler: {navn}")

        for kilde in CSE_IDS:
            links = find_links(navn, kilde)
            print(f"  [{kilde}] Fundet {len(links)} link(s)")

            pris_fundet = None

            for link in links:
                if "/products/" not in link:
                    print(f"    ✘ Ignorerer ikke-produktlink: {link}")
                    continue

                pris = hent_pris_fra_url(link, kilde)

                if pris is not None:
                    print(f"    ✔ Pris: {pris} kr fra {link}")
                    pris_fundet = pris
                    break  # Brug første gyldige pris
                else:
                    print(f"    ✘ Pris ikke fundet for: {link}")

            if pris_fundet is not None:
                vin_resultat["konkurrenter"][kilde] = f"{pris_fundet} kr"
                if billigste_pris is None or pris_fundet < billigste_pris:
                    billigste_pris = pris_fundet
                    billigste_kilde = kilde
            else:
                vin_resultat["konkurrenter"][kilde] = None

        vin_resultat["billigste"] = billigste_kilde
        resultat.append(vin_resultat)

    return resultat

from cse import CSE_IDS, find_links
from scraper import hent_pris_fra_url

def sammenlign_med_konkurrenter(vine):
    resultat = []

    for vin in vine:
        navn = vin.get("navn")
        egen_pris = vin.get("egen_pris", "-")
        vin_resultat = {"navn": navn, "egen_pris": egen_pris}

        billigste = None
        billigste_kilde = None

        print(f"\n→ Behandler: {navn}")

        for kilde in CSE_IDS:
            links = find_links(navn, kilde)
            print(f"  [{kilde}] Fundet {len(links)} link(s)")

            for link in links:
                if "/products/" not in link:
                    print(f"    ✘ Ignorerer ikke-produktlink: {link}")
                    continue

                pris = hent_pris_fra_url(link, kilde)

                if pris is not None:
                    print(f"    ✔ Pris: {pris} kr fra {link}")
                    if billigste is None or pris < billigste:
                        billigste = pris
                        billigste_kilde = kilde
                else:
                    print(f"    ✘ Pris ikke fundet for: {link}")

        vin_resultat["konkurrent_pris"] = (
            f"{billigste} kr ({billigste_kilde})" if billigste else "Ikke fundet"
        )

        resultat.append(vin_resultat)

    return resultat

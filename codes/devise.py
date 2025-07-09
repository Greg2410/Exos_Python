
import requests


def convertisseur_monnaie():
    """fonction qui prendra un dictionnaire
    contenant une monnaie et son taux et permettra de convertir
    une monnaie en une autre"""

#   Url de l'API
    url = "https://happyapi.fr/api/devises"

    response = requests.get(url)

    monnaies = {}
    if response.status_code == 200:
        data = response.json()

        devises = data["result"]["result"]["devises"]

        for devise in devises:
            code = devise["codeISODevise"]
            taux = devise["taux"]
            monnaies[code] = {"code": code, "taux": taux}
    else:
        print(f"Erreur lors de la requête : {response.status_code}")

    for code, infos in monnaies.items():
        print(f"{code} : {infos}")

    monnaie_base = input("De quelle monnaie partez vous ? ")
    valeur_base = 0
    valeur_user = int(input("Combien voulez vous convertir ? "))
    monnaie_user = input("En quelle monnaie voulez vous "
                         "convertir cette valeur ? ")
    monnaie_echange = monnaies[monnaie_user]["taux"]

    if monnaie_base in monnaies and monnaie_user in monnaies:
        valeur_base = monnaie_echange / monnaies[monnaie_base]["taux"]
        print(valeur_base)
    else:
        print("Cette monnaie n'a pas été ajoutée")

    print(f"{valeur_user} {monnaie_base} en {monnaie_user} :\n ",
          valeur_user*valeur_base)


convertisseur_monnaie()

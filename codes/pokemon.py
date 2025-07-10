import requests
import random
import time

# --- FONCTIONS DE BASE ---

type_avantage = {
    "feu": ["plante", "glace"],
    "eau": ["feu", "roche"],
    "plante": ["eau", "roche"],
    "électrik": ["eau", "vol"],
    "sol": ["feu", "électrik", "roche"],
    # Ajoute ce que tu veux
}

def choisir_pokemon(deck):
    print("\n🃏 Choisissez votre Pokémon pour ce combat :")
    for i, p in enumerate(deck):
        print(f"{i+1}. {p['nom']} ({p['type']}) ATQ:{p['attaque']} DEF:{p['defense']} PV:{p['hp']}")
    choix = int(input("Numéro : ")) - 1
    return deck.pop(choix)


def get_type_bonus(att_type, def_type):
    if def_type in type_avantage.get(att_type, []):
        return 2  # super efficace
    elif att_type in type_avantage.get(def_type, []):
        return 0.5  # pas très efficace
    return 1  # neutre


def get_pokemon_data(id):
    stats_url = f"https://pokeapi.co/api/v2/pokemon/{id}"
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{id}"

    stats_resp = requests.get(stats_url)
    species_resp = requests.get(species_url)

    if stats_resp.status_code == 200 and species_resp.status_code == 200:
        stats_data = stats_resp.json()
        species_data = species_resp.json()

        nom_fr = next((n["name"] for n in species_data["names"] if n["language"]["name"] == "fr"), "Inconnu")
        hp = next(stat["base_stat"] for stat in stats_data["stats"] if stat["stat"]["name"] == "hp")
        attaque = next(stat["base_stat"] for stat in stats_data["stats"] if stat["stat"]["name"] == "attack")
        defense = next(stat["base_stat"] for stat in stats_data["stats"] if stat["stat"]["name"] == "defense")
        type_ = stats_data["types"][0]["type"]["name"]

        return {
            "nom": nom_fr.capitalize(),
            "type": type_,
            "hp": hp,
            "attaque": attaque,
            "defense": defense
        }
    return None

def build_deck(nombre=3):
    deck = []
    ids = random.sample(range(1, 152), nombre)
    for i in ids:
        pokemon = get_pokemon_data(i)
        if pokemon:
            deck.append(pokemon)
    return deck

def afficher_deck(deck):
    print("\n🃏 Vos cartes Pokémon :")
    for i, p in enumerate(deck):
        print(f"{i+1}. {p['nom']} ({p['type']}) - ATQ: {p['attaque']} | DEF: {p['defense']} | PV: {p['hp']}")

def combat(p1, p2):
    print(f"\n⚔️ {p1['nom']} ({p1['type']}) VS {p2['nom']} ({p2['type']})")
    time.sleep(1)
    
    bonus1 = get_type_bonus(p1["type"], p2["type"])
    bonus2 = get_type_bonus(p2["type"], p1["type"])

    degats1 = max(int((p1["attaque"] * bonus1) - p2["defense"]), 0)
    degats2 = max(int((p2["attaque"] * bonus2) - p1["defense"]), 0)

    p2["hp"] -= degats1
    p1["hp"] -= degats2
    
    if bonus1 == 2:
        print(f"🟢 {p1['nom']} est super efficace contre {p2['nom']} !")
    elif bonus1 == 0.5:
        print(f"🔴 {p1['nom']} n’est pas très efficace contre {p2['nom']}...")

    print(f"➡️ {p1['nom']} inflige {degats1} dégâts à {p2['nom']}")
    print(f"⬅️ {p2['nom']} inflige {degats2} dégâts à {p1['nom']}")

    print(f"❤️ {p1['nom']} : {p1['hp']} PV")
    print(f"❤️ {p2['nom']} : {p2['hp']} PV")

    if p1["hp"] <= 0 and p2["hp"] <= 0:
        print("💥 Match nul !")
    elif p1["hp"] <= 0:
        print(f"❌ {p1['nom']} est K.O. !")
    elif p2["hp"] <= 0:
        print(f"✅ {p2['nom']} est K.O. !")

# --- MENU INTERACTIF ---

def menu():
    deck_joueur = build_deck()
    while True:
        print("\n====== MENU POKÉMON ======")
        print("1. Voir mon deck")
        print("2. Lancer un combat")
        print("3. Nouveau deck")
        print("4. Quitter")
        choix = input("👉 Choisissez une option : ")

        if choix == "1":
            afficher_deck(deck_joueur)

        elif choix == "2":
            bot_deck = build_deck()
            print("\n🧠 Combat contre le bot !")
            for i in range(len(deck_joueur)):
                print(f"\n--- Tour {i+1} ---")
                combat(deck_joueur[i], bot_deck[i])
                time.sleep(1.5)

        elif choix == "3":
            print("🔁 Nouveau deck généré !")
            deck_joueur = build_deck()

        elif choix == "4":
            print("👋 Au revoir dresseur !")
            break

        else:
            print("⛔ Choix invalide. Essayez encore.")

# --- LANCEMENT DU JEU ---
menu()

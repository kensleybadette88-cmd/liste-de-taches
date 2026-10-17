"""Gestionnaire de tâches en ligne de commande avec sauvegarde JSON."""
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("taches.json")

def charger_taches():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("Sauvegarde invalide; une nouvelle liste démarre.")
        return []

def sauvegarder_taches(taches):
    DATA_FILE.write_text(json.dumps(taches, ensure_ascii=False, indent=2), encoding="utf-8")

def afficher_taches(taches):
    print()
    if not taches:
        print("Aucune tâche pour le moment.")
        return
    print("Mes tâches")
    for numero, tache in enumerate(taches, start=1):
        etat = "terminée" if tache["terminee"] else "à faire"
        print("{}. [{}] {}".format(numero, etat, tache["texte"]))

def demander_numero(taches, action):
    afficher_taches(taches)
    if not taches:
        return None
    try:
        numero = int(input("Numéro de la tâche à {} : ".format(action)))
    except ValueError:
        print("Entre un numéro valide.")
        return None
    if numero < 1 or numero > len(taches):
        print("Ce numéro ne correspond à aucune tâche.")
        return None
    return numero - 1

def main():
    taches = charger_taches()
    while True:
        print()
        print("=== Ma liste de tâches ===")
        print("1. Ajouter une tâche")
        print("2. Afficher les tâches")
        print("3. Terminer une tâche")
        print("4. Supprimer une tâche")
        print("5. Quitter")
        choix = input("Choisis une option (1-5) : ").strip()
        if choix == "1":
            texte = input("Nouvelle tâche : ").strip()
            if texte:
                taches.append({"texte": texte, "terminee": False})
                sauvegarder_taches(taches)
                print("Tâche ajoutée.")
            else:
                print("La tâche ne peut pas être vide.")
        elif choix == "2":
            afficher_taches(taches)
        elif choix == "3":
            index = demander_numero(taches, "terminer")
            if index is not None:
                taches[index]["terminee"] = True
                sauvegarder_taches(taches)
                print("Tâche terminée !")
        elif choix == "4":
            index = demander_numero(taches, "supprimer")
            if index is not None:
                retiree = taches.pop(index)
                sauvegarder_taches(taches)
                print("Tâche supprimée : {}".format(retiree["texte"]))
        elif choix == "5":
            print("À bientôt !")
            break
        else:
            print("Choisis un nombre de 1 à 5.")

if __name__ == "__main__":
    main()

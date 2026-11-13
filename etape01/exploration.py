import csv
from collections import Counter

# Chemins des fichiers CSV
FICHIER_SITES = "data/sites.csv"
FICHIER_MATERIEL = "data/materiel.csv"
FICHIER_RESERVATIONS = "data/reservations.csv"
FICHIER_ASSOCIATIONS = "data/associations.csv"


# 1. Lire un fichier CSV
def lire_csv(chemin):
    with open(chemin, encoding="utf-8", newline="") as fichier:
        return list(csv.DictReader(fichier))


# 2. Compter les valeurs d'une colonne
def compter_par(lignes, colonne):
    compteur = Counter()

    for ligne in lignes:
        compteur[ligne[colonne]] += 1

    return dict(compteur)


# 3. Additionner les quantités par groupe
def total_par(lignes, colonne_groupe, colonne_valeur):
    totaux = {}

    for ligne in lignes:
        groupe = ligne[colonne_groupe]
        valeur = int(ligne[colonne_valeur])

        if groupe not in totaux:
            totaux[groupe] = 0

        totaux[groupe] += valeur

    return totaux


# 4. Classe Site
class Site:
    def __init__(self, code_site, nom, commune,
                 annee_ouverture, surface_m2):
        self.code_site = code_site
        self.nom = nom
        self.commune = commune
        self.annee_ouverture = int(annee_ouverture)
        self.surface_m2 = int(surface_m2)

    def anciennete(self, annee_reference):
        return annee_reference - self.annee_ouverture

    def __str__(self):
        return f"{self.code_site} - {self.nom} ({self.commune}), {self.surface_m2} m2"


# 5. Réservations en cours
def reservations_en_cours(reservations):
    resultat = []

    for reservation in reservations:
        if reservation["date_retour_reelle"].strip() == "":
            resultat.append(reservation)

    return resultat


# 6. Programme principal
def main():

    sites = lire_csv(FICHIER_SITES)
    materiels = lire_csv(FICHIER_MATERIEL)
    reservations = lire_csv(FICHIER_RESERVATIONS)
    associations = lire_csv(FICHIER_ASSOCIATIONS)

    # Nombre de lignes
    print("=== NOMBRE DE LIGNES ===")
    print("Sites :", len(sites))
    print("Matériels :", len(materiels))
    print("Réservations :", len(reservations))
    print("Associations :", len(associations))

    # Affichage des sites
    print("\n=== SITES ===")

    for ligne in sites:
        site = Site(
            ligne["code_site"],
            ligne["nom"],
            ligne["commune"],
            ligne["annee_ouverture"],
            ligne["surface_m2"]
        )

        print(site, "- Ancienneté :", site.anciennete(2026), "ans")

    # Réservations par site
    print("\n=== RÉSERVATIONS PAR SITE ===")

    comptes = compter_par(reservations, "code_site")

    for code, nombre in sorted(comptes.items(), key=lambda x: x[1], reverse=True):
        print(code, ":", nombre)

    # Quantités par site
    print("\n=== QUANTITÉS PAR SITE ===")

    quantites = total_par(reservations, "code_site", "quantite")

    for code, total in sorted(quantites.items(), key=lambda x: x[1], reverse=True):
        print(code, ":", total)

    # Matériels par état
    print("\n=== MATÉRIELS PAR ÉTAT ===")

    etats = compter_par(materiels, "etat")

    for etat, nombre in etats.items():
        print(etat, ":", nombre)

    # Catégories différentes
    print("\n=== CATÉGORIES ===")

    categories = compter_par(materiels, "categorie")
    print("Nombre de catégories différentes :", len(categories))

    # Réservations en cours
    print("\n=== RÉSERVATIONS EN COURS ===")

    en_cours = reservations_en_cours(reservations)
    print("Nombre de réservations en cours :", len(en_cours))


# 7. Lancement du programme
if __name__ == "__main__":
    main()

import os
import sys
import re
import parcourir


def dictionnaire_final(echantillon_et_replicats) -> dict:
    resultat_final = {}  # Initialise le dictionnaire final pour stocker les résultats par échantillon.

    # Crée un dictionnaire pour chaque échantillon.
    for echantillon, chemins_rep in echantillon_et_replicats.items():
        resultat_echantillon = {}

        # Pour chaque réplicat, il crée un nouveau dictionnaire.
        for chemin_r in chemins_rep:
            valeurs_colonnes = {}
            nom_fichier = chemin_r.split('/')[-1]  # Récupère le nom du fichier à partir du chemin complet.

            with open(chemin_r, 'r') as f:
                for ligne in f:
                    if ligne.startswith('#'):
                        continue
                    # Divise la ligne en colonnes en utilisant la tabulation comme séparateur.
                    colonne = ligne.split('\t')
                    # Récupère les valeurs des colonnes 1, 4 et 7.
                    valeur_colonne_1, valeur_colonne_4, valeur_colonne_7 = colonne[1], colonne[4], colonne[7]

                    # Si la valeur de la colonne 4 est '<DUP>', '<DEL>', ou '<INS>'.
                    if valeur_colonne_4 in ('<DUP>', '<DEL>', '<INS>'):
                        # Récupère la partie du texte après "SVLEN=" jusqu'au prochain ";" dans la colonne 7 pour avoir la longueur de la variation (seulement si cette valeur existe).
                        svlen = valeur_colonne_7.split('SVLEN=')[1].split(';')[0] if 'SVLEN=' in valeur_colonne_7 else None

                        # Si la valeur de la colonne 1 n'est pas déjà présente, crée une nouvelle entrée dans le dictionnaire.
                        if valeur_colonne_1 not in valeurs_colonnes:
                            valeurs_colonnes[valeur_colonne_1] = []

                        # Ajoute la valeur de la colonne 1, 4 et SVLEN à la liste correspondante dans le dictionnaire.
                        valeurs_colonnes[valeur_colonne_1].append((valeur_colonne_4, svlen))
                    # Si la valeur de la colonne 4 est une séquence de nucléotides.
                    else:
                        # Si la valeur de la colonne 1 n'est pas déjà présente, crée une nouvelle entrée dans le dictionnaire.
                        if valeur_colonne_1 not in valeurs_colonnes:
                            valeurs_colonnes[valeur_colonne_1] = []
                            
                        # Ajoute la valeur de la colonne 1 et 4 à la liste correspondante dans le dictionnaire.
                        valeurs_colonnes[valeur_colonne_1].append(valeur_colonne_4)

            # Associe les valeurs des colonnes 1 et 4 au nom du fichier.
            if valeurs_colonnes:
                resultat_echantillon[nom_fichier] = valeurs_colonnes

        # Modification des clés du dictionnaire final pour enlever les informations supplémentaires et rendre la sortie plus visible
        resultat_echantillon_modifie = {}
        for cle, valeur in resultat_echantillon.items():
            nouvelle_cle = cle.split('.')[0] if '.' in cle else cle
            resultat_echantillon_modifie[nouvelle_cle] = valeur

        if resultat_echantillon_modifie:
            resultat_final[echantillon] = resultat_echantillon_modifie
    return resultat_final


# Exemple : 
# resultat_final = {
#		'P30': {
#			'P30-1': {'22620': ['GTAGTAGTGGT'], '37879': ['TGTGGTG', 'TGTGTGTG', 'TGACAGAGAC']}, 
#			'P30-2': {'196282': ['TCTCTCTCAAA'], '178820': [('<INS>', '112')]}}, 
#		'P15': {
#			'P15-3': {'3243': ['TAATGTGATGGGCCTCGGCG'], '11375': ['GTAAGTACATCAATTAAGACAGAC']}, 
#			'P15-1': {'1210': ['TGTGATGTATTG'], '11375': ['GTAAGGTGTCCTCC']}, 
#			'P15-2': {'11375': ['GTAAGTACATCTGT'], '178820': [('<DEL>', '-12')]}}                                              
# }


def comparer_dictionnaires(resultat_final: dict, decalage, pourcentage) -> dict:
    comparaisons = {}  # Dictionnaire pour stocker les comparaisons

    for echantillon, fichiers_valeurs in resultat_final.items():  # Parcourt les échantillons et leurs fichiers de valeurs
        fichiers = list(fichiers_valeurs)  # Liste des fichiers pour un échantillon donné

        for i, fichier_1 in enumerate(fichiers):  # Itération sur les fichiers de cet échantillon
            valeurs_1 = fichiers_valeurs[fichier_1]  # Récupère les valeurs du premier fichier

            for fichier_2 in fichiers[i + 1:]:  # Compare ce fichier avec les fichiers restants dans l'échantillon
                valeurs_2 = fichiers_valeurs[fichier_2]  # Récupère les valeurs du deuxième fichier

                # Vérifie si les valeurs sont : '<DUP>', '<DEL>', ou '<INS>'
                if valeurs_1.get(0) and valeurs_2.get(0) and valeurs_1[0][0] in ('<DUP>', '<DEL>', '<INS>') and valeurs_1[0][0] == valeurs_2[0][0]:
                    # Compte les occurrences de clés avec des conditions spécifiques
                    compteur_communs = sum(
                        1
                        for cle1, valeur1 in valeurs_1.items()
                        for cle2, valeur2 in valeurs_2.items()
                        if (
                            abs(int(cle1) - int(cle2)) <= decalage  # Vérifie l'écart entre les clés
                            and valeur1[0] == valeur2[0]  # Vérifie les valeurs de la colonne 4 (position et type de variation)
                            and valeur1[0][1] == valeur2[0][1]  # Vérifie les longueurs (SVLEN)
                        )
                    )
                else:  # Autres valeurs (séquences de nucléotides)
                    # Compte les clés similaires avec des critères différents
                    compteur_communs = sum(
                        1
                        for cle1, valeur1 in valeurs_1.items()
                        for cle2, valeur2 in valeurs_2.items()
                        if (
                            abs(int(cle1) - int(cle2)) <= decalage  # Vérifie l'écart entre les clés
                            and (sum(1 for a, b in zip(valeur1, valeur2) if a == b) / max(len(valeur1), len(valeur2))) * 100 >= pourcentage  # Vérifie un pourcentage de similarité
                            and cle1 == cle2  # Vérifie si les clés sont identiques
                        )
                    )

                cle_comparaison = f"{fichier_1} - {fichier_2}"  # Clé pour stocker la comparaison

                comparaisons[cle_comparaison] = compteur_communs  # Stocke le résultat dans le dictionnaire des comparaisons

    return comparaisons  # Renvoie le dictionnaire contenant les comparaisons


# Exemple :
# comparaisons = {  'P30-1 - P30-2': 0,
#                   'P30-1 - P30-3': 7, 
#                   'P30-2 - P30-3': 0, 
#                   'P15-3 - P15-1': 14, 
#                   'P15-3 - P15-2': 3, 
#                   'P15-1 - P15-2': 3       }  


def mise_en_forme(comparaisons: dict,str) -> None:
    print ("\n"+str)
    print("\n-----------------------Premier echantillon-----------------------")
    cles = list(comparaisons.keys())  # Extraction des clés du dictionnaire 'comparaisons' et conversion en liste

    for i, cle in enumerate(cles):
        print("le couple de réplicat : ", cle, "a un nombre de variant commun égal à : ", comparaisons[cle])
        # Trouve l'index du premier "-" dans la clé
        premier_tiret_cle = cle.index('-') if '-' in cle else len(cle)
        
        # Vérifie si ce n'est pas le dernier élément et si la sous-chaîne jusqu'au premier "-" est différente de la suivante
        if i < len(cles) - 1 and cle[:premier_tiret_cle] != cles[i + 1][:premier_tiret_cle]:
            print("\n-----------------------Echantillon suivant-----------------------")
            # Affiche une ligne de séparation entre les échantillons distincts


def main():
    # Prend le chemin du fichier en argument
    chemin = sys.argv[1]

    # Vérifie le nombre d'arguments passés en ligne de commande
    if len(sys.argv) == 4:  # S'il y a 4 arguments, alors :
        decalage = int(sys.argv[2])  # Prend le deuxième argument comme décalage
        pourcentage = int(sys.argv[3])  # Prend le troisième argument comme pourcentage
    elif len(sys.argv) == 3:  # Sinon, s'il y a 3 arguments :
        decalage = int(sys.argv[2])  # Prend le deuxième argument comme décalage
        pourcentage = 100  # Initialise le pourcentage à 100
    else:  # Sinon (moins de 3 arguments) :
        decalage = 0  # Initialise le décalage à 0
        pourcentage = 100  # Initialise le pourcentage à 100
    
    # Crée une phrase décrivant les paramètres
    phrase = "Bienvenue dans ce programme qui analyse le nombre de variants communs entre chaque réplicats deux à deux au sein d'un échantillon.\nLes paramètres sont les suivants :\n\n\tPourcentage de similarité minimum entre les séquences communes : " + str(pourcentage) + "\n\tDécalage d'alignement maximum entre les variants (shift) : " + str(decalage)
    
    # Obtient les échantillons et les réplicats à partir du chemin fourni
    echantillon_et_replicats = parcourir.parc(chemin)
    
    # Compare les dictionnaires pour trouver les variants communs
    resultat = comparer_dictionnaires(dictionnaire_final(echantillon_et_replicats), decalage, pourcentage)
    
    # Affiche les résultats avec la phrase décrivant les paramètres
    mise_en_forme(resultat, phrase)

if __name__ == "__main__":
    # Si le fichier est exécuté en tant que programme principal, appelle la fonction main
    main()



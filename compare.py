
import os
import sys
import re
import parcourir



# echantillon_et_replicats = {'P30': ['Data/Data/P30/P30-1.trimed1000.sv_sniffles.vcf', 'Data/Data/P30/P30-2.trimed1000.sv_sniffles.vcf', 'Data/Data/P30/P30-3.trimed1000.sv_sniffles.vcf'],
#                             'P15': ['Data/Data/P15/P15-3.trimed1000.sv_sniffles.vcf', 'Data/Data/P15/P15-1.trimed1000.sv_sniffles.vcf', 'Data/Data/P15/P15-2.trimed1000.sv_sniffles.vcf']} 


def dictionnaire_final(echantillon_et_replicats) -> dict:  
    resultat_final = {}  # Initialise le dictionnaire final pour stocker les résultats par échantillon.

    # Itère à travers chaque échantillon et ses chemins associés.
    for echantillon, chemins in echantillon_et_replicats.items():
        resultat_echantillon = {}  # Initialise le dictionnaire pour stocker les résultats de l'échantillon.

        # Itère à travers chaque chemin de l'échantillon.
        for chemin in chemins:
            valeurs_colonne_1_4 = {}  # Initialise le dictionnaire pour stocker les valeurs des colonnes 1 et 4.
            nom_fichier = chemin.split('/')[-1]  # Récupère le nom du fichier à partir du chemin complet.

            # Ouvre le fichier correspondant en mode lecture.
            with open(chemin, 'r') as f:
                # Itère à travers chaque ligne du fichier.
                for ligne in f:
                    # Vérifie si la ligne commence par '#' et continue à la prochaine si c'est le cas.
                    if ligne.startswith('#'):
                        continue
                    
                    # Divise la ligne en colonnes en utilisant la tabulation comme séparateur.
                    colonne = ligne.split('\t')
                    # Récupère les valeurs des colonnes 1 et 4 en supprimant les espaces vides autour.
                    valeur_colonne_1, valeur_colonne_4 = colonne[1].strip(), colonne[4].strip()
                    
                    # Vérifie si la valeur de la colonne 4 n'est pas '<DUP>', '<DEL>', ou '<INS>'.
                    if valeur_colonne_4 not in ('<DUP>', '<DEL>', '<INS>'):
                        # Si la valeur de la colonne 1 n'est pas déjà présente, crée une nouvelle entrée dans le dictionnaire.
                        if valeur_colonne_1 not in valeurs_colonne_1_4:
                            valeurs_colonne_1_4[valeur_colonne_1] = []
                        
                        # Ajoute la valeur de la colonne 4 à la liste correspondante dans le dictionnaire.
                        valeurs_colonne_1_4[valeur_colonne_1].append(valeur_colonne_4)
            
            # Associe les valeurs des colonnes 1 et 4 au nom du fichier.
            if valeurs_colonne_1_4:
                resultat_echantillon[nom_fichier] = valeurs_colonne_1_4
        
        # Associe les résultats de l'échantillon au dictionnaire final.
        if resultat_echantillon:
            resultat_final[echantillon] = resultat_echantillon
    
    return resultat_final  # Renvoie le dictionnaire final contenant les résultats pour chaque échantillon.


# resultat_final = {
#		'P30': {
#			'P30-1.trimed1000.sv_sniffles.vcf': {'22620': ['GTAGTAGTGGT'], '37879': ['TGTGGTG', 'TGTGTGTG', 'TGACAGAGAC']}, 
#			'P30-2.trimed1000.sv_sniffles.vcf': {'196282': ['TCTCTCTCAAA']}}, 
#		'P15': {
#			'P15-3.trimed1000.sv_sniffles.vcf': {'3243': ['TAATGTGATGGGCCTCGGCG'], '11375': ['GTAAGTACATCAATTAAGACAGAC']}, 
#			'P15-1.trimed1000.sv_sniffles.vcf': {'1210': ['TGTGATGTATTG'], '11375': ['GTAAGGTGTCCTCC']}, 
#			'P15-2.trimed1000.sv_sniffles.vcf': {'11375': ['GTAAGTACATCTGT']}}                                              
# }


def comparer_dictionnaires(resultat_final: dict) -> dict:
    comparaisons = {}  # Initialise le dictionnaire pour stocker les résultats de comparaison.

    # Itère à travers chaque échantillon et les fichiers associés avec les valeurs de la colonne 1 et 4.
    for echantillon, fichiers_valeurs in resultat_final.items():
        fichiers = list(fichiers_valeurs)  # Récupère les noms des fichiers du dictionnaire.

        # Itère à travers chaque paire de fichiers.
        for i, fichier_1 in enumerate(fichiers):
            valeurs_1 = fichiers_valeurs[fichier_1]  # Récupère les valeurs associées au fichier 1.

            # Itère à travers les autres fichiers (à partir du fichier suivant après fichier_1).
            for fichier_2 in fichiers[i + 1:]:
                valeurs_2 = fichiers_valeurs[fichier_2]  # Récupère les valeurs associées au fichier 2.

                # Compte le nombre de clé valeurs identiques entre les fichiers 1 et 2.
                compteur_communs = sum(
                    1 # On incrémente de 1 à chaque fois qu'on trouve une valeur commune
                    for cle1, valeur1 in valeurs_1.items()
                    for cle2, valeur2 in valeurs_2.items()
                    if int(cle1) == int(cle2) and valeur1 == valeur2
                )
                # Crée une clé pour le dictionnaire de comparaison.
                cle_comparaison = f"{fichier_1} - {fichier_2}"
                # Ajoute le nombre de valeurs communes au dictionnaire de comparaison.
                comparaisons[cle_comparaison] = compteur_communs

    return comparaisons  # Renvoie le dictionnaire contenant les comparaisons entre les fichiers.



def comparer_dictionnaires_v2(resultat_final: dict) -> dict:
    comparaisons = {}  # Initialise le dictionnaire pour stocker les résultats de comparaison.

    # Itère à travers chaque échantillon et les fichiers associés avec les valeurs de la colonne 1 et 4.
    for echantillon, fichiers_valeurs in resultat_final.items():
        fichiers = list(fichiers_valeurs)  # Récupère les noms des fichiers du dictionnaire.

        # Itère à travers chaque paire de fichiers.
        for i, fichier_1 in enumerate(fichiers):
            valeurs_1 = fichiers_valeurs[fichier_1]  # Récupère les valeurs associées au fichier 1.

            # Itère à travers les autres fichiers (à partir du fichier suivant après fichier_1).
            for fichier_2 in fichiers[i + 1:]:
                valeurs_2 = fichiers_valeurs[fichier_2] # Récupère les valeurs associées au fichier 2.

                # Compte le nombre de clé identiques (à 10 nucléotides près) avec des valeurs identiques entre les fichiers 1 et 2.
                compteur_communs = sum(
                    1
                    for cle1, valeur1 in valeurs_1.items()
                    for cle2, valeur2 in valeurs_2.items()
                    if abs(int(cle1) - int(cle2)) <= 10 and valeur1 == valeur2 # Vérifie si la différence entre les valeurs de la colonne 1 est inférieure ou égale à 10.
                )

                # Crée une clé pour le dictionnaire de comparaison.
                cle_comparaison = f"{fichier_1} - {fichier_2}"
                # Ajoute le nombre de valeurs communes au dictionnaire de comparaison.
                comparaisons[cle_comparaison] = compteur_communs

    return comparaisons  # Renvoie le dictionnaire contenant les comparaisons entre les fichiers.



def comparer_dictionnaires_v3(resultat_final: dict) -> dict:
    comparaisons = {}  # Initialise le dictionnaire pour stocker les résultats de comparaison.

    # Itère à travers chaque échantillon et les fichiers associés avec les valeurs de la colonne 1 et 4.
    for echantillon, fichiers_valeurs in resultat_final.items():
        fichiers = list(fichiers_valeurs)  # Récupère les noms des fichiers du dictionnaire.

        # Itère à travers chaque paire de fichiers.
        for i, fichier_1 in enumerate(fichiers):
            valeurs_1 = fichiers_valeurs[fichier_1]  # Récupère les valeurs associées au fichier 1.

            # Itère à travers les autres fichiers (à partir du fichier suivant après fichier_1).
            for fichier_2 in fichiers[i + 1:]:
                valeurs_2 = fichiers_valeurs[fichier_2] # Récupère les valeurs associées au fichier 2.

                # Compte le nombre de clé identiques (à 10 nucléotides près) avec des valeurs identiques entre les fichiers 1 et 2.
                compteur_communs = sum(
                        1
                        for cle1, valeur1 in valeurs_1.items()
                        for cle2, valeur2 in valeurs_2.items()
                        for a, b in zip(valeur1, valeur2)
                        if abs(int(cle1) - int(cle2)) <= 10 and (sum(1 for a, b in zip(valeur1, valeur2) if a == b) / max(len(valeur1), len(valeur2))) * 100 >= 75
                    )
                # Crée une clé pour le dictionnaire de comparaison.
                cle_comparaison = f"{fichier_1} - {fichier_2}"
                # Ajoute le nombre de valeurs communes au dictionnaire de comparaison.
                comparaisons[cle_comparaison] = compteur_communs

    return comparaisons  # Renvoie le dictionnaire contenant les comparaisons entre les fichiers.




# comparaisons = {  'P30-1.trimed1000.sv_sniffles.vcf - P30-2.trimed1000.sv_sniffles.vcf': 0,
#                   'P30-1.trimed1000.sv_sniffles.vcf - P30-3.trimed1000.sv_sniffles.vcf': 6, 
#                   'P30-2.trimed1000.sv_sniffles.vcf - P30-3.trimed1000.sv_sniffles.vcf': 0, 
#                   'P15-3.trimed1000.sv_sniffles.vcf - P15-1.trimed1000.sv_sniffles.vcf': 14, 
#                   'P15-3.trimed1000.sv_sniffles.vcf - P15-2.trimed1000.sv_sniffles.vcf': 3, 
#                   'P15-1.trimed1000.sv_sniffles.vcf - P15-2.trimed1000.sv_sniffles.vcf': 3        }  



def mise_en_forme(comparaisons: dict,str) -> None:
    print ("\n"+str)
    print("\n-----------------------Premier echantillon-----------------------")
    cles = list(comparaisons.keys())  # Extraction des clés du dictionnaire 'comparaisons' et conversion en liste

    # Itère à travers chaque clé et son index dans la liste 'cles'
    for i, cle in enumerate(cles):
        print("le couple de réplicat : ", cle, "a un nombre de variant commun égal à : ", comparaisons[cle])
        # Trouve l'index du premier "-" dans la clé
        premier_tiret_cle = cle.index('-') if '-' in cle else len(cle)
        
        # Vérifie si ce n'est pas le dernier élément et si la sous-chaîne jusqu'au premier "-" est différente de la suivante
        if i < len(cles) - 1 and cle[:premier_tiret_cle] != cles[i + 1][:premier_tiret_cle]:
            print("\n-----------------------Echantillon suivant-----------------------")
            # Affiche une ligne de séparation entre les échantillons distincts


def main():
    chemin = sys.argv[1]
    echantillon_et_replicats = parcourir.parc(chemin)
    resultat = comparer_dictionnaires(dictionnaire_final(echantillon_et_replicats))
    resultat2 = comparer_dictionnaires_v2(dictionnaire_final(echantillon_et_replicats))
    resultat3 = comparer_dictionnaires_v3(dictionnaire_final(echantillon_et_replicats))
    mise_en_forme(resultat, "Version 1 : ")
    mise_en_forme(resultat2, "Version 2 : ")
    mise_en_forme(resultat3, "Version 3 : ")
    
if __name__ == "__main__": # Si la fonction sépciale s'appelle main alors il faut lancer la fonction main
    main() 

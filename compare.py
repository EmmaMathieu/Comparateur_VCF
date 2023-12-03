
import os
import sys
import re
import parcourir


def dictionnaire_final(echantillon_et_replicats) -> dict: # Cette fonction prend en entrée un dictionnaire contenant des échantillons et le path+leurs réplicats associés et renvoie un dictionnaire contenant des échantillons et le path+leurs réplicats associés avec les valeurs de la colonne 1 et 4.
    resultat_final = {} # Initialise un dictionnaire vide pour stocker les échantillons et leurs réplicats avec les valeurs de la colonne 1 et 4.
    for echantillon, chemins in echantillon_et_replicats.items(): # Itère à travers les échantillons et les chemins associés.
        dic = {} # Initialise un dictionnaire vide pour stocker les échantillons et les chemins associés avec les valeurs de la colonne 1 et 4.
        for chemin in chemins: # Itère à travers les chemins associés aux échantillons.
            nom_fichier = chemin.split('/')[-1] # Sépare le chemin du nom de fichier et récupère le nom de fichier.
            valeurs_colonne_1_4 = {} # Initialise un dictionnaire vide pour stocker les valeurs de la colonne 1 et 4.
            with open(chemin, 'r') as f: # Ouvre le fichier en mode lecture.
                for ligne in f: # Itère à travers les lignes du fichier.
                    if ligne.startswith('#'): # Vérifie si la ligne commence par '#'.
                        continue # Passe à la ligne suivante.
                    colonne = ligne.split('\t') # Sépare la ligne par tabulation et récupère les éléments dans une liste.
                    valeur_colonne_1, valeur_colonne_4 = map(str.strip, (colonne[1], colonne[4])) # Récupère les valeurs de la colonne 1 et 4.
                    if valeur_colonne_4 not in ('<DUP>', '<DEL>', '<INS>'): # Vérifie si la valeur de la colonne 4 n'est pas '<DUP>', '<DEL>' ou '<INS>'.
                        valeurs_colonne_1_4.setdefault(valeur_colonne_1, []).append(valeur_colonne_4) # Crée une nouvelle entrée dans le dictionnaire pour cette valeur de la colonne 1.
            dic[nom_fichier] = valeurs_colonne_1_4 # Ajoute les valeurs de la colonne 1 et 4 au dictionnaire.
        resultat_final[echantillon] = dic # Ajoute les échantillons et les chemins associés avec les valeurs de la colonne 1 et 4 au dictionnaire.
    return resultat_final # Renvoie le dictionnaire contenant les échantillons et les chemins associés avec les valeurs de la colonne 1 et 4.


# resultat_final = {
#		'P30': {
#			'P30-1.trimed1000.sv_sniffles.vcf': {'22620': ['GTAGTAGTGGT'], '37879': ['TGTGGTG', 'TGTGTGTG', 'TGACAGAGAC']}, 
#			'P30-2.trimed1000.sv_sniffles.vcf': {'196282': ['TCTCTCTCAAA']}}, 
#		'P15': {
#			'P15-3.trimed1000.sv_sniffles.vcf': {'3243': ['TAATGTGATGGGCCTCGGCG'], '11375': ['GTAAGTACATCAATTAAGACAGAC']}, 
#			'P15-1.trimed1000.sv_sniffles.vcf': {'1210': ['TGTGATGTATTG'], '11375': ['GTAAGGTGTCCTCC']}, 
#			'P15-2.trimed1000.sv_sniffles.vcf': {'11375': ['GTAAGTACATCTGT']}}                                              
# } 


def comparer_dictionnaires(resultat_final: dict) -> dict: # Cette fonction prend en entrée un dictionnaire contenant des échantillons et le path+leurs réplicats associés avec les valeurs de la colonne 1 et 4 et renvoie un dictionnaire contenant des échantillons et le path+leurs réplicats associés avec les valeurs de la colonne 1 et 4 et le nombre de variant commun.
    comparaisons = {} # Initialise un dictionnaire vide pour stocker les échantillons et les chemins associés avec les valeurs de la colonne 1 et 4 et le nombre de variant commun.
    for echantillon, dic in resultat_final.items(): # Itère à travers les échantillons et les chemins associés avec les valeurs de la colonne 1 et 4.
        fichiers = list(dic) # Récupère les noms des fichiers du dictionnaire.
        for i, fichier_1 in enumerate(fichiers): # Itère à travers les noms des fichiers du dictionnaire.
            valeurs_1 = dic[fichier_1] # Récupère les valeurs associées au fichier 1.
            for fichier_2 in fichiers[i + 1:]: # Itère à travers les noms des fichiers du dictionnaire à partir du fichier 1.
                valeurs_2 = dic[fichier_2] # Récupère les valeurs associées au fichier 2.
                compteur_communs = sum(1 for k, v in valeurs_1.items() if k in valeurs_2 and set(v) == set(valeurs_2.get(k, []))) # Compte le nombre de variant commun.
                cle_comparaison = f"{fichier_1} - {fichier_2}" # Crée une nouvelle clé pour le dictionnaire.
                comparaisons[cle_comparaison] = compteur_communs # Ajoute le nombre de variant commun au dictionnaire.
    return comparaisons # Renvoie le dictionnaire contenant les échantillons et les chemins associés avec les valeurs de la colonne 1 et 4 et le nombre de variant commun.


# comparaisons = {  'P30-1.trimed1000.sv_sniffles.vcf - P30-2.trimed1000.sv_sniffles.vcf': 0,
#                   'P30-1.trimed1000.sv_sniffles.vcf - P30-3.trimed1000.sv_sniffles.vcf': 6, 
#                   'P30-2.trimed1000.sv_sniffles.vcf - P30-3.trimed1000.sv_sniffles.vcf': 0, 
#                   'P15-3.trimed1000.sv_sniffles.vcf - P15-1.trimed1000.sv_sniffles.vcf': 14, 
#                   'P15-3.trimed1000.sv_sniffles.vcf - P15-2.trimed1000.sv_sniffles.vcf': 3, 
#                   'P15-1.trimed1000.sv_sniffles.vcf - P15-2.trimed1000.sv_sniffles.vcf': 3        }  


def comparer_dictionnaires_v2(resultat_final: dict) -> dict:
    comparaisons = {}
    for echantillon, dic in resultat_final.items():
        fichiers = list(dic)
        for i, (fichier_1, valeurs_1) in enumerate(dic.items()): # Itère à travers les noms des fichiers et les valeurs associées.
            for fichier_2, valeurs_2 in list(dic.items())[i + 1:]: # Itère à travers les noms des fichiers et les valeurs associées à partir du fichier 1.
                compteur_communs = sum(
                    1
                    for k1, v1 in valeurs_1.items()
                    for k2, v2 in valeurs_2.items()
                    if abs(int(k1) - int(k2)) <= 10 and set(v1) == set(v2) # Vérifie si la différence entre les valeurs de la colonne 1 est inférieure ou égale à 10.
                )
                cle_comparaison = f"{fichier_1} - {fichier_2}"
                comparaisons[cle_comparaison] = compteur_communs
    return comparaisons

"""
# Définition de la fonction 'mise_en_forme' prenant un argument 'comparaison' de type dictionnaire
def mise_en_forme(comparaison):
    # Affichage d'une ligne de séparation pour marquer le début du traitement des données
    print("-----------------------Premier echantillon-----------------------")

    # Extraction des clés du dictionnaire 'comparaison' et conversion en liste
    cles = list(comparaison.keys())

    # Itération à travers la liste 'cles' avec indice et valeur associée
    for i, cle in enumerate(cles):
        # Affichage des informations relatives à chaque paire clé-valeur du dictionnaire
        print("le couple de réplicat : ", cle, "a un nombre de variant commun égal à : ", comparaison[cle])
        
        # Vérification pour savoir s'il s'agit du dernier élément et si la première partie de la clé est différente de la suivante
        if i < len(cles) - 1 and cle[:3] != cles[i + 1][:3]:
            # Affichage d'une ligne de séparation entre les groupes de données distincts
            print("\n-----------------------Echantillon suivant-----------------------")  
"""


def mise_en_forme(comparaisons: dict) -> None : 
    print("-----------------------Premier echantillon-----------------------")
    cles = list(comparaisons.keys())
    for i, cle in enumerate(cles):
        print("le couple de réplicat : ", cle, "a un nombre de variant commun égal à : ", comparaisons[cle])
        if i < len(cles) - 1 and cle[:3] != cles[i + 1][:3]:
            print("\n-----------------------Echantillon suivant-----------------------") 


def main():
    chemin = sys.argv[1]
    echantillon_et_replicats = parcourir.parc(chemin)
    resultat = comparer_dictionnaires(dictionnaire_final(echantillon_et_replicats))
    #resultat = comparer_dictionnaires_v2(dictionnaire_final(echantillon_et_replicats))
    mise_en_forme(resultat)
    
if __name__ == "__main__": #si la fonction sépciale s'appelle main alors il faut lancer la fonction main
    main() 

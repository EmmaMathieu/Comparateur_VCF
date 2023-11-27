
import os
import sys
import re
import parcourir

# echantillon_et_replicats = {'P30': ['Data/Data/P30/P30-1.trimed1000.sv_sniffles.vcf', 'Data/Data/P30/P30-2.trimed1000.sv_sniffles.vcf', 'Data/Data/P30/P30-3.trimed1000.sv_sniffles.vcf'],
#                             'P15': ['Data/Data/P15/P15-3.trimed1000.sv_sniffles.vcf', 'Data/Data/P15/P15-1.trimed1000.sv_sniffles.vcf', 'Data/Data/P15/P15-2.trimed1000.sv_sniffles.vcf']} 

# Cette fonction prend un dictionnaire contenant des échantillons et leurs chemins de fichiers associés et renvoie un dictionnaire final organisé.
def dictionnaire_final(echantillon_et_replicats) -> dict:
    resultat_final = {}  # Initialise le dictionnaire final pour stocker les résultats
    
    # Boucle à travers chaque échantillon et ses chemins de fichiers associés
    for echantillon, chemins in echantillon_et_replicats.items():
        dic = {}  # Initialise un dictionnaire pour stocker les informations de chaque fichier associé à un échantillon
        
        # Boucle à travers chaque chemin de fichier pour un échantillon donné
        for chemin in chemins:
            nom_fichier = chemin.split('/')[-1]  # Récupère le nom du fichier à partir du chemin
            
            valeurs_colonne_1_4 = {}  # Dictionnaire pour regrouper les valeurs de colonne 4 par colonne 1
            
            # Ouvre le fichier et lit chaque ligne pour récupérer les valeurs nécessaires
            with open(chemin, 'r') as f:
                for ligne in f:
                    if ligne.startswith('#'):  # Ignore les lignes commençant par '#'
                        continue
                    colonne = ligne.split('\t')  # Sépare les éléments de la ligne par tabulation
                    valeur_colonne_1 = colonne[1].strip()  # Récupère la valeur de la colonne 1
                    valeur_colonne_4 = colonne[4].strip()  # Récupère la valeur de la colonne 4
                    
                    # Vérifie si la valeur de la colonne 4 n'est pas l'une des valeurs spécifiées
                    if valeur_colonne_4 not in ('<DUP>', '<DEL>', '<INS>'):
                        if valeur_colonne_1 in valeurs_colonne_1_4:
                            valeurs_colonne_1_4[valeur_colonne_1].append(valeur_colonne_4)
                        else:
                            valeurs_colonne_1_4[valeur_colonne_1] = [valeur_colonne_4]

            # Ajoute le dictionnaire de regroupement colonne 1 - colonne 4 au dictionnaire global avec le nom du fichier comme clé
            dic[nom_fichier] = valeurs_colonne_1_4

        # Ajoute le dictionnaire associé à l'échantillon au dictionnaire final
        resultat_final[echantillon] = dic

    return resultat_final  # Renvoie le dictionnaire final avec les informations organisées



def comparer_dictionnaires(resultat_final) -> dict:
    comparaisons = {}

    # Comparer chaque paire de fichiers d'un même dictionnaire
    for echantillon, dic in resultat_final.items():
        fichiers = list(dic.keys())  # Récupérer les noms des fichiers du dictionnaire
        nb_fichiers = len(fichiers)

        # Comparaison entre les fichiers du même dictionnaire
        for i in range(nb_fichiers):
            for j in range(i + 1, nb_fichiers):
                fichier_1 = fichiers[i]
                fichier_2 = fichiers[j]

                valeurs_1 = dic[fichier_1]
                valeurs_2 = dic[fichier_2]

                # Comparaison des ensembles clé:valeur
                compteur_communs = sum(1 for k, v in valeurs_1.items() if k in valeurs_2 and set(v) == set(valeurs_2[k]))

                # Clé pour identifier la comparaison
                cle_comparaison = f"{fichier_1} - {fichier_2}"
                comparaisons[cle_comparaison] = compteur_communs

    return comparaisons





def comparer_dictionnaires_v2(resultat_final) -> dict:
    comparaisons = {}  # Dictionnaire pour stocker les résultats des comparaisons

    # Comparer chaque paire de fichiers d'un même dictionnaire
    for echantillon, dic in resultat_final.items():
        fichiers = list(dic.keys())  # Récupérer les noms des fichiers du dictionnaire
        nb_fichiers = len(fichiers)

        # Comparaison entre les fichiers du même dictionnaire
        for i in range(nb_fichiers):
            for j in range(i + 1, nb_fichiers):
                fichier_1 = fichiers[i]
                fichier_2 = fichiers[j]

                valeurs_1 = dic[fichier_1]  # Obtenir les valeurs associées au fichier 1
                valeurs_2 = dic[fichier_2]  # Obtenir les valeurs associées au fichier 2

                # Comparaison des ensembles clé:valeur
                compteur_communs = sum(  # Utilisation de la fonction sum pour compter le nombre d'éléments respectant une condition
                    1  # On ajoute 1 à chaque fois que la condition est vraie
                    for k1, v1 in valeurs_1.items()  # Parcours des clés et valeurs du fichier 1
                    for k2, v2 in valeurs_2.items()  # Parcours des clés et valeurs du fichier 2
                    if abs(int(k1) - int(k2)) <= 10 and set(v1) == set(v2)  # Condition pour considérer les paires clé:valeur comme identiques
                )

                # Clé pour identifier la comparaison
                cle_comparaison = f"{fichier_1} - {fichier_2}"
                comparaisons[cle_comparaison] = compteur_communs  # Stocker le nombre de paires identiques dans le dictionnaire de résultats

    return comparaisons  # Retourner le dictionnaire de résultats des comparaisons



def comparer_dictionnaires_v3(resultat_final) -> dict:
    comparaisons = {}  # Dictionnaire pour stocker les résultats des comparaisons

    # Comparer chaque paire de fichiers d'un même dictionnaire
    for echantillon, dic in resultat_final.items():
        fichiers = list(dic.keys())  # Récupérer les noms des fichiers du dictionnaire
        nb_fichiers = len(fichiers)

        # Comparaison entre les fichiers du même dictionnaire
        for i in range(nb_fichiers):
            for j in range(i + 1, nb_fichiers):
                fichier_1 = fichiers[i]
                fichier_2 = fichiers[j]

                valeurs_1 = dic[fichier_1]  # Obtenir les valeurs associées au fichier 1
                valeurs_2 = dic[fichier_2]  # Obtenir les valeurs associées au fichier 2

                # Calcul du pourcentage de similitude
                similitude = sum(
                    1 for v1, v2 in zip(valeurs_1.values(), valeurs_2.values()) if v1 == v2
                ) / max(len(valeurs_1.values()), len(valeurs_2.values())) * 100

                # Incrémentation du compteur si le pourcentage de similitude est >= 75%
                if similitude >= 75:
                    cle_comparaison = f"{fichier_1} - {fichier_2}"
                    comparaisons[cle_comparaison] = 1  # Incrémenter de 1 pour les paires qui dépassent le seuil de similitude

    return comparaisons  # Retourner le dictionnaire de résultats des comparaisons


def main():
    chemin = sys.argv[1]
    echantillon_et_replicats = parcourir.parc(chemin)
    resultat = comparer_dictionnaires_v3(dictionnaire_final(echantillon_et_replicats))
    print (resultat)
    
    #si la fonction sépciale s'appelle main alors il faut lancer la fonction main

if __name__ == "__main__":
    main()
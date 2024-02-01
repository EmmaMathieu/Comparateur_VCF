import os
import sys
import re
import parcourir


def dictionnaire_final(echantillon_et_replicats) -> dict:
    resultat_final = {}

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
                    colonne = ligne.split('\t')
                    valeur_colonne_1, valeur_colonne_4, valeur_colonne_7 = colonne[1], colonne[4], colonne[7]

                    freq = valeur_colonne_7.split('AF=')[1].split(';')[0] if 'AF=' in valeur_colonne_7 else None

                    # Si la valeur de la colonne 4 est '<DUP>', '<DEL>', ou '<INS>'.
                    if valeur_colonne_4 in ('<DUP>', '<DEL>', '<INS>'):
                        # Récupère la partie du texte après "SVLEN=" jusqu'au prochain ";" dans la colonne 7 pour avoir la longueur de la variation (seulement si cette valeur existe).
                        svlen = valeur_colonne_7.split('SVLEN=')[1].split(';')[0] if 'SVLEN=' in valeur_colonne_7 else None

                        # Si la valeur de la colonne 1 n'est pas déjà présente, crée une nouvelle entrée dans le dictionnaire.
                        if valeur_colonne_1 not in valeurs_colonnes:
                            valeurs_colonnes[valeur_colonne_1] = []

                        # Ajoute la valeur de la colonne 1, 4 et SVLEN à la liste correspondante dans le dictionnaire.
                        valeurs_colonnes[valeur_colonne_1].append([(valeur_colonne_4, svlen), freq])

                    # Si la valeur de la colonne 4 est une séquence de nucléotides.
                    else:
                        # Si la valeur de la colonne 1 n'est pas déjà présente, crée une nouvelle entrée dans le dictionnaire.
                        if valeur_colonne_1 not in valeurs_colonnes:
                            valeurs_colonnes[valeur_colonne_1] = []
                        # Ajoute la valeur de la colonne 1 et 4 à la liste correspondante dans le dictionnaire.
                        valeurs_colonnes[valeur_colonne_1].append([valeur_colonne_4, freq])
                        # print(valeurs_colonnes[valeur_colonne_1])

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

    for fichiers_valeurs in resultat_final.values():  # Parcourt les échantillons et leurs fichiers de valeurs
        fichiers = list(fichiers_valeurs)  # Liste des fichiers pour un échantillon donné

        for i, fichier_1 in enumerate(fichiers):  # Itération sur les fichiers de cet échantillon

            valeurs_1 = fichiers_valeurs[fichier_1]  # Récupère les valeurs du premier fichier

            for fichier_2 in fichiers[i + 1:]:  # Compare ce fichier avec les fichiers restants dans l'échantillon
                valeurs_2 = fichiers_valeurs[fichier_2]  # Récupère les valeurs du deuxième fichier

                lval1 = []
                for cle,val in valeurs_1.items():
                    for v in val:
                        lval1.append((cle, v[0]))

                lval2 = []
                for cle,val in valeurs_2.items():
                    for v in val:
                        lval2.append((cle, v[0]))
                
                compteur_communs = sum(
                    1
                    for cle1, valeur1 in lval1
                    for cle2, valeur2 in lval2
                    if( abs(int(cle1) - int(cle2)) <= decalage and
                        ((type(valeur1) == tuple and type(valeur2) == tuple and valeur1[0] == valeur2[0] and valeur1[1] == valeur2[1]) or
                        ((sum(1 for a, b in zip(valeur1, valeur2) if a == b) / max(len(valeur1), len(valeur2))) * 100 >= pourcentage))
                        )
                    )


                # Vérifie si les valeurs sont : '<DUP>', '<DEL>', ou '<INS>'
                
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


def mise_en_forme(comparaisons: dict, str) -> str:
    resultat = "\n" + str + "\n"
    resultat += "\n-----------------------Premier echantillon-----------------------\n"
    cles = list(comparaisons.keys())

    for i, cle in enumerate(cles):
        resultat += f"le couple de réplicat : {cle} a un nombre de variant commun égal à : {comparaisons[cle]}\n"
        premier_tiret_cle = cle.index('-') if '-' in cle else len(cle)
        
        if i < len(cles) - 1 and cle[:premier_tiret_cle] != cles[i + 1][:premier_tiret_cle]:
            resultat += "\n-----------------------Echantillon suivant-----------------------\n"
    return resultat

def ecrire_dans_fichier(chemin_sortie: str, resultat_concatene: str):
    with open(chemin_sortie, 'w') as fichier:
        fichier.write(resultat_concatene)


def main():
    # Premier fichier est le chemin du repertoire des vcf
    chemin = sys.argv[1]

    if len(sys.argv) == 4: 
        decalage = int(sys.argv[2])  # Prend le deuxième argument comme décalage
        pourcentage = int(sys.argv[3])  # Prend le troisième argument comme pourcentage
    elif len(sys.argv) == 3:  
        decalage = int(sys.argv[2])  # Prend le deuxième argument comme décalage
        pourcentage = 100  # Initialise le pourcentage à 100
    else: 
        decalage = 0  # Initialise le décalage à 0
        pourcentage = 100  # Initialise le pourcentage à 100   

    phrase = "Bienvenue dans ce programme qui analyse le nombre de variants communs entre chaque réplicats deux à deux au sein d'un échantillon.\nLes paramètres sont les suivants :\n\n\tPourcentage de similarité minimum entre les séquences communes : " + str(pourcentage) + "\n\tDécalage d'alignement maximum entre les variants (shift) : " + str(decalage)
    echantillon_et_replicats = parcourir.parc(chemin)    
    
    resultat = comparer_dictionnaires(dictionnaire_final(echantillon_et_replicats), decalage, pourcentage)    
   
    # print(mise_en_forme(resultat, phrase))


    # Chemin où sauvegarder le fichier de resultat
    chemin_sortie = "Resultat_comparaison_VCF.txt"

    # Écriture le contenu dans le fichier
    ecrire_dans_fichier(chemin_sortie, mise_en_forme(resultat, phrase))

if __name__ == "__main__":
    # Si le fichier est exécuté en tant que programme principal, appelle la fonction main
    main()



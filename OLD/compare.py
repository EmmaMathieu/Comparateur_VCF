
import os
import sys
import re
import parcourir



# echantillon_et_replicats = {          'P30': {'1.trimed1000.sv_sniffles', '3.trimed1000.sv_sniffles', '2.trimed1000.sv_sniffles'}, 
#                                       'P15': {'1.trimed1000.sv_sniffles', '3.trimed1000.sv_sniffles', '2.trimed1000.sv_sniffles'}}
def lire_ranger_fichier (nom_fichier):
    dic = {}
    with open(nom_fichier, 'r') as f:
        for ligne in f:
            if ligne.startswith('#'):
                continue
            colonne = ligne.split('\t')
            if '<DUP>' not in colonne[4] and '<DEL>' not in colonne[4]: 
                dic[colonne[1]] = colonne[4]

    
    for cle, valeur in dic.items():
        print(f"{cle}: {valeur}\n")


    #return dic
        

def dictionnaire_final (echantillon_et_replicats) -> {}: 
    liste_dictionnaire_d = {}
    
    lire_ranger_fichier(echantillon_et_replicats)


    #for each {} in echantillon_et_replicats : 
        #if  
    
        

        
    #PARTIE 1
    #for each valeur d'une clef du dictionnaire en entrée, faire un dictionnaire avec pour clef la position (tabulation n°2 dans le document), 
    #et pour valeur la tabulation 5 (Seulement si ce qui est dans la tabulation 5 est différent de <DUP> et <DEL>), on rajoute qu'on prend pas en compte les lignes qui commencent par #
    #chaque dictionnaire crée aura pour nom le nom de l'échantillon et réplicat 
    #si il y a plusieurs clef qui sont les memes, regrouper les valeurs dans une seule clef
    #en sortie on a donc une liste de dictionnaire qui ressemble a : 
    #liste_dictionnaire_d = [{'P30-1' : {1 : AAAGTCC},{145 : AAAGTCC, AATCGGGG, AAAAA}}, {'P30-2' : {155 : AAAGTCC},{2943 : AAAGTGG, AAAAA}}.....]
    
    #PARTIE 2
    #liste_dictionnaire_dictionnaire_d = [{{}}]

    # on fait autant de dictionnaire de dictionnaire qu'il y a de comparaison de réplicat 2 à 2,
    # pour deux dictionnaire de liste_dictionnaire_d deux a deux, on regarde 
        # si, a la meme position il y a la meme insertion, dans le dictionnaire qui a le nom de l'échantillon, 
        # il faut mettre en clef le nom des deux réplicats comparés et en valeur le nombre de variant commun (qui ont exactement la meme position et la meme séquence d'insertion)
    
    #le résultat doit ressembler à : 
    # liste_dictionnaire_dictionnaire = [{'P30' : {P30-1 & P30-2 : 6},{P30-2 & P30-3 : 9},{P30-1 & P30-3 : 19}}, {'P15' : {P15-1 & P15-2 : 9},{P15-2 & P15-3 : 4},{P15-1 & P15-3 : 0}}]

    #liste_dictionnaire_d = echantillon_et_replicats
    # print liste_dictionnaire_dictionnaire
    return liste_dictionnaire_d
    
def main():
    chemin = sys.argv[1]
    echantillon_et_replicats = parcourir.parc(chemin)
    resultat = dictionnaire_final(echantillon_et_replicats)
    #debug
    print (resultat)
    #si la fonction sépciale s'appelle main alors il faut lancer la fonction main

if __name__ == "__main__":
    main()
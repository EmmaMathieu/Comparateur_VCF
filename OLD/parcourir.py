import os
import sys

def parc(chemin) -> {}:
    # Initialisation de la liste pour stocker les fichiers VCF
    fichiers_vcf = []

    # Initialisation du dictionnaire pour stocker les réplicats
    echantillon_et_replicats = {}

    # os.walk(chemin) prend en paramètre le chemin, et il ressort UN tuple (une raçine (str), une liste de dossiers(strs), une liste de fichiers(strs))
    for raçine, dossier, fichiers in os.walk(chemin):
        for fichier in fichiers:
            if fichier.endswith(".vcf"):
                # Si le fichier est un fichier VCF, l'ajouter à la liste
                fichiers_vcf.append(fichier)
                
                # Récupérer le nom du fichier sans l'extension
                # os.path.splitext(fichier) est une fonction qui prend en paramètre un nom de fichier 
                # et qui retourne un tuple avec le nom du fichier et son extension
                # [0] est le nom du fichier et [1] est l'extension
                nom_fichier = os.path.splitext(fichier)[0]
                
                # coupe le strig donné en entrée et retourne une liste des éléments séparés par le caractère "-"
                elements = nom_fichier.split("-")
                # si le cardinal de la liste élément est égal à 2, alors on affecte le premier a echantillon et le deuxième a numéro_replicat
                if len(elements) == 2:
                    echantillon, numero_replicat = elements
                    # Vérifier si la clé existe déjà dans le dictionnaire
                    if echantillon in echantillon_et_replicats:
                        # Si oui, ajouter numero_replicat à l'ensemble existant
                        echantillon_et_replicats[echantillon].add(numero_replicat)
                    else:
                        # Si non, créer une nouvelle entrée avec un ensemble contsenant numero_replicat
                        echantillon_et_replicats[echantillon] = {numero_replicat}
    return echantillon_et_replicats

#fonction principale pour pouvoir appeler les autres fonction dans le script
def main():
    chemin = sys.argv[1]
    resultat = parc(chemin)
    #debug
    #print (resultat)
#si la fonction sépciale s'appelle main alors il faut lancer la fonction main
if __name__ == "__main__":
    main()
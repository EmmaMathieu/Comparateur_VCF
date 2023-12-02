import os
import sys


# Cette fonction prend en entrée un chemin de type string et renvoie un dictionnaire contenant des échantillons et le path+leurs réplicats associés.
def parc(chemin : str) -> dict:
    echantillon_et_replicats = {}  # Initialise un dictionnaire vide pour stocker les échantillons et leurs réplicats
    
    # Parcours de tous les fichiers et dossiers à partir du chemin donné
    for racine, dossiers, fichiers in os.walk(chemin):
        # Parcours de chaque fichier dans les fichiers de chaque dossier
        for fichier in fichiers:
            # Vérifie si le fichier a l'extension ".vcf"
            if fichier.endswith(".vcf"):
                chemin_complet = os.path.join(racine, fichier)  # Chemin complet du fichier
                
                nom_fichier = os.path.splitext(fichier)[0]  # Récupère le nom du fichier sans extension
                elements = nom_fichier.split("-")  # Sépare le nom en éléments en utilisant le caractère "-"
                
                # Vérifie s'il y a deux éléments dans la séparation
                if len(elements) == 2:
                    echantillon, numero_replicat = elements  # Sépare le nom de l'échantillon et le numéro de réplicat
                    
                    chemin_complet_vcf = os.path.join(racine, fichier)  # Chemin complet du fichier VCF
                    
                    # Vérifie si l'échantillon existe déjà dans le dictionnaire
                    if echantillon in echantillon_et_replicats:
                        # Ajoute le chemin complet du fichier VCF à la liste des fichiers pour cet échantillon
                        echantillon_et_replicats[echantillon].append(chemin_complet_vcf)
                    else:
                        # Crée une nouvelle entrée dans le dictionnaire pour cet échantillon
                        echantillon_et_replicats[echantillon] = [chemin_complet_vcf]

    return echantillon_et_replicats  # Renvoie le dictionnaire contenant les échantillons et leurs fichiers VCF associés

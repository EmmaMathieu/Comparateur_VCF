import os


# Cette fonction prend en entrée le dossier initial qui est de type string et renvoie un dictionnaire contenant une liste de Path concaténé avec les noms des fichiers VCF associés.
def parc(chemin: str) -> dict: 
    echantillon_et_replicats = {} 
    for racine, dossiers, fichiers in os.walk(chemin): # Cette boucle for utilise la fonction os.walk() pour parcourir récursivement le répertoire spécifié par le chemin. À chaque itération, elle récupère trois valeurs : racine (le répertoire actuel), dossiers (les sous-répertoires dans ce répertoire) et fichiers (les fichiers dans ce répertoire).
        for fichier in fichiers: # Itère à travers la liste des fichiers obtenus à partir de la boucle précédente.
            if fichier.endswith(".vcf"): # Vérifie si le fichier a l'extension ".vcf"
                chemin_complet_vcf = os.path.join(racine, fichier) # Combine le chemin du répertoire racine (ici Data) avec le chemin du fichier et le nom du fichier (c'est une unique chose pour le programme).
                elements = os.path.splitext(fichier)[0].split("-") # Sépare le nom de fichier de son extension. Cela renvoie le nom de fichier sans l'extension.
                if len(elements) == 2: # Vérifie s'il y a deux éléments dans la séparation
                    echantillon_et_replicats.setdefault(elements[0], []).append(chemin_complet_vcf) # Crée une nouvelle entrée dans le dictionnaire pour cet échantillon
    return echantillon_et_replicats # Renvoie le dictionnaire contenant les échantillons et leurs réplicats associés


# echantillon_et_replicats = {'P30': ['Data/Data/P30/P30-1.trimed1000.sv_sniffles.vcf', 'Data/Data/P30/P30-2.trimed1000.sv_sniffles.vcf', 'Data/Data/P30/P30-3.trimed1000.sv_sniffles.vcf'],
#                             'P15': ['Data/Data/P15/P15-3.trimed1000.sv_sniffles.vcf', 'Data/Data/P15/P15-1.trimed1000.sv_sniffles.vcf', 'Data/Data/P15/P15-2.trimed1000.sv_sniffles.vcf']} 

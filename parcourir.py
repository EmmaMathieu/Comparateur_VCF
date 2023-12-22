import os

def parc(chemin: str) -> dict: 
    echantillon_et_replicats = {} 
    for racine, dossiers, fichiers in os.walk(chemin): 
        # Utilise os.walk() pour parcourir récursivement le répertoire spécifié par le chemin.
        # À chaque itération, récupère racine, dossiers et fichiers.
        for fichier in fichiers: 
            # Itère à travers la liste des fichiers obtenus précédemment.
            if fichier.endswith(".vcf"): 
                chemin_complet_vcf = os.path.join(racine, fichier) 
                # Concatène le chemin relatif à la racine et le chemin du fichier.
                elements = os.path.splitext(fichier)[0].split("-") 
                # Divise le nom du fichier en deux parties : échantillon et numéro de réplicat.
                if len(elements) == 2: 
                    # Si les deux parties existent.
                    echantillon_et_replicats.setdefault(elements[0], []).append(chemin_complet_vcf) 
                    # Crée une nouvelle entrée dans le dictionnaire ou ajoute le chemin_complet_vcf à une liste existante.
    return echantillon_et_replicats

# Exemple :
# echantillon_et_replicats ={   'P30': ['/home/emmamlinux/documents/Aide/Data/Data/P30/P30-1.trimed1000.sv_sniffles.vcf', 
#                                       '/home/emmamlinux/documents/Aide/Data/Data/P30/P30-2.trimed1000.sv_sniffles.vcf', 
#                                       '/home/emmamlinux/documents/Aide/Data/Data/P30/P30-3.trimed1000.sv_sniffles.vcf'], 
#                               'P15': ['/home/emmamlinux/documents/Aide/Data/Data/P15/P15-3.trimed1000.sv_sniffles.vcf', 
#                                       '/home/emmamlinux/documents/Aide/Data/Data/P15/P15-1.trimed1000.sv_sniffles.vcf', 
#                                       '/home/emmamlinux/documents/Aide/Data/Data/P15/P15-2.trimed1000.sv_sniffles.vcf']} 
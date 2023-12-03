import os



def parc(chemin: str) -> dict: 
    echantillon_et_replicats = {} 
    for racine, dossiers, fichiers in os.walk(chemin): 
        # Cette boucle for utilise la fonction os.walk() pour parcourir récursivement le répertoire spécifié par le chemin. 
        # À chaque itération, elle récupère trois valeurs : racine (le répertoire actuel), dossiers (les sous-répertoires dans ce répertoire) et fichiers (les fichiers dans ce répertoire).
        for fichier in fichiers: # Itère à travers la liste des fichiers obtenus à partir de la boucle précédente.
            if fichier.endswith(".vcf"): 
                chemin_complet_vcf = os.path.join(racine, fichier) 
                # .join concatène le chemin relatif a mon projet de la raçine (juste le nom du premier dossier) et le chemin du fichier (qui contient aussi le nom du fichier)
                elements = os.path.splitext(fichier)[0].split("-") 
                # os.path.splitext() divise le chemin du fichier fichier en deux parties : le nom du fichier et son extension. 
                # En utilisant l'index [0], on récupère la première partie, c'est-à-dire le nom du fichier sans l'extension.
                # .split() divise le nom du fichier en deux parties (liste): le nom de l'échantillon et le numéro du réplicat.
                if len(elements) == 2: 
                    echantillon_et_replicats.setdefault(elements[0], []).append(chemin_complet_vcf) 
                    # La méthode setdefault() est une méthode qui permet de définir une valeur par défaut pour une clé donnée si cette clé n'existe pas déjà dans le dictionnaire. 
                    # Elle prend deux arguments : la clé que vous voulez vérifier et la valeur par défaut à assigner si la clé n'existe pas.
                    # Si la clé n'existe pas, setdefault() crée une nouvelle entrée dans le dictionnaire avec elements[0] comme clé (le nom de l'échantillon) et une liste vide comme valeur par défaut. 
                    # Ensuite, avec la méthode .append, chemin_complet_vcf est ajouté à cette liste comme valeur.
    return echantillon_et_replicats # Renvoie le dictionnaire contenant les échantillons et leurs réplicats associés


# echantillon_et_replicats = {'P30': ['Data/Data/P30/P30-1.trimed1000.sv_sniffles.vcf', 'Data/Data/P30/P30-2.trimed1000.sv_sniffles.vcf', 'Data/Data/P30/P30-3.trimed1000.sv_sniffles.vcf'],
#                             'P15': ['Data/Data/P15/P15-3.trimed1000.sv_sniffles.vcf', 'Data/Data/P15/P15-1.trimed1000.sv_sniffles.vcf', 'Data/Data/P15/P15-2.trimed1000.sv_sniffles.vcf']} 

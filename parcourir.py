import os
import sys

def parc(chemin) -> dict:
    echantillon_et_replicats = {}
    for racine, dossiers, fichiers in os.walk(chemin):
        for fichier in fichiers:
            if fichier.endswith(".vcf"):
                chemin_complet = os.path.join(racine, fichier)
                
                nom_fichier = os.path.splitext(fichier)[0]
                elements = nom_fichier.split("-")
                
                if len(elements) == 2:
                    echantillon, numero_replicat = elements
                    
                    chemin_complet_vcf = os.path.join(racine, fichier)
                    
                    if echantillon in echantillon_et_replicats:
                        echantillon_et_replicats[echantillon].append(chemin_complet_vcf)
                    else:
                        echantillon_et_replicats[echantillon] = [chemin_complet_vcf]

    return echantillon_et_replicats

#fonction principale pour pouvoir appeler les autres fonction dans le script
def main():
    chemin = sys.argv[1]
    resultat = parc(chemin)
    #debug
    print (resultat)
#si la fonction sépciale s'appelle main alors il faut lancer la fonction main
if __name__ == "__main__":
    main()
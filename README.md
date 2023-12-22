# Nom du Programme

## Description

Ce programme compare les fichiers VCF issus de réplicats biologiques provenant d'un même échantillon afin d'identifier les variants communs entre ces réplicats. Ce test a une grande spécificité mais une faible sensibilité.

## Utilisation

### Prérequis

- Python 3.x
- Modules requis : [Liste des modules avec les versions](lien_vers_requirements.txt)

### Installation

1. Clonez ce dépôt : `git clone https://github.com/votre-utilisateur/votre-projet.git`
2. Installez les dépendances : `pip install -r requirements.txt`

### Fichiers Principaux

Ce projet contient trois fichiers principaux :

- `parcourir.py` : Fichier Python pour parcourir le dossier en argument et stocker une liste des réplicats ainsi que leurs chemins.
- `compare.py` : Fichier Python pour comparer les réplicats et déterminer les variants communs au sein d'un même échantillon.
- `main.sh` : Fichier bash pour exécuter le programme principal en utilisant le terminal.

### Exécution du Programme

Pour exécuter ce programme sous un environnement Linux, utilisez le fichier bash `main.sh` dans le terminal avec la commande :

1. `./main.sh ./cheminAbsoluDossierContenantLesFichiersAComparer`
2. Pour trouver le chemin absolu, utilisez `pwd` dans le terminal après vous être placé dans le dossier, puis ajoutez `/NomDuDossierContenantLesFichiersAComparer`.
3. Le programme accepte également l'option `-h` pour afficher l'aide. Pour afficher l'aide, exécutez : `./main.sh -h`

#### Options

- `-h`, `--help` : Affiche l'aide sur l'utilisation du programme.

### Interprétation Biologique

A. Moins de similarité entre réplicats :
   - Une faible similarité peut indiquer des variations pouvant résulter de mutations aléatoires lors de l'amplification par exemple et donc une faible qualité des échantillons et des réplicats de ceux-ci.
   - Conditions variables : Des environnements variables ou des traitements différents des échantillons peuvent conduire à des différences génétiques entre les réplicats.

B. Plus de similarité entre réplicats :
   - Peut indiquer des conditions expérimentales plus homogènes pour chaque réplicat.
   - Peut indiquer une ou plusieurs véritables variations génétiques par rapport au génome de référence (Vous pouvez donc écarter l'hypothèse d'une variation génétique due à une erreur de manipulation ou d'amplification).

Ces interprétations sont des pistes pour comprendre la signification biologique des résultats de comparaison entre réplicats, mais des analyses plus poussées et une intégration de données supplémentaires peuvent être nécessaires pour une interprétation complète.

### Attention

- Vos fichiers de réplicats doivent être au format VCF (.vcf) avec un nom comme ceci : `P+numéro_echantillon-numéro_réplicat.vcf`.
- Assurez-vous que le fichier ait les permissions d'exécution, sinon, utilisez la commande suivante pour donner la permission : `chmod +777 main.sh compare.py parcourir.py`

## Support

Pour toute question ou difficulté dans l'utilisation du programme, contactez : [Nom de l'auteur](mailto:emma.mathieu02@etu.umontpellier.fr)

Merci d'avoir lu et utilisé ce programme.


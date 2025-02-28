# Comparateur_VCF

## Description

Ce programme compare les fichiers VCF dans un dossier spécifié pour analyser les variants communs entre les réplicats d'un échantillon. 
Ce programme crée un document nommé Resultat_comparaison_VCF.txt dans le répertoire de vos données a comparer, ce document contiendra les informations de sortie du programme qui seront également affichée sur le terminal

Pour déterminer si les variants sont identiques, le programme prendra en compte :

1. La séquence et la position si la séquence de variation est spécifiée.
2. Le type, la position et la longueur si la séquence de variation n'est pas spécifiée.

## Utilisation

### Prérequis

- Environnement Linux
- Python 3

### Installation

1. Clonez ce dépôt : `git clone https://github.com/EmmaMathieu/Comparateur_VCF.git`
2. Ouvrez un terminal dans le dossier cloné.

Pour ce programme, il est inutile d'installer des modules supplémentaires.

### Fichiers Principaux

- `main.sh` : Fichier bash pour exécuter le programme principal en utilisant le terminal.
- `parcourir.py` : Fichier Python pour parcourir le dossier en argument et stocker une liste des réplicats ainsi que leurs chemins.
- `compare.py` : Fichier Python pour comparer les réplicats et déterminer les variants communs au sein d'un même échantillon.

### Exécution du Programme

Pour exécuter ce programme sous un environnement Linux, utilisez le fichier bash `main.sh` dans le terminal avec la commande :

1. `./main.sh ./chemin/du/dossier/contenant/les/fichiers/a/comparer décalage_max pourcentage_d'identité_min`
   - Pour trouver le chemin absolu, utilisez `pwd` dans le terminal après vous être placé dans le dossier, puis ajoutez `/Nom/du/dossier/contenant/les/fichiers/VCF/a/comparer`.

#### Options

- `-h`, `--help` : Affiche l'aide sur l'utilisation du programme.

### Interprétations biologiques

A. Moins de similarité entre réplicats :
   - Une faible similarité peut indiquer des variations pouvant résulter de mutations aléatoires lors de l'amplification par exemple et donc une faible qualité des échantillons et des réplicats de ceux-ci.
   - Conditions variables : Des environnements variables ou des traitements différents des échantillons peuvent conduire à des différences génétiques entre les réplicats.

B. Plus de similarité entre réplicats :
   - Peut indiquer des conditions expérimentales plus homogènes pour chaque réplicat.
   - Peut indiquer une ou plusieurs véritables variations génétiques par rapport au génome de référence (Vous pouvez donc écarter l'hypothèse d'une variation génétique due à une erreur de manipulation ou d'amplification).

Ces interprétations sont des pistes pour comprendre la signification biologique des résultats de comparaison entre réplicats, mais des analyses plus poussées et une intégration de données supplémentaires peuvent être nécessaires pour une interprétation complète.

### Attention

- Vos fichiers doivent être au format VCF (.vcf) avec un nom comme ceci : `P+numéro_echantillon-numéro_réplicat.vcf`.
- Assurez-vous que le fichier ait les permissions d'exécution, sinon, utilisez la commande suivante pour donner la permission : `chmod +777 main.sh compare.py parcourir.py`

## Support

Pour toute question ou difficulté dans l'utilisation du programme, contactez Emma MATHIEU : emma.mathieu02@etu.umontpellier.fr

Merci d'avoir lu et utilisé ce programme.

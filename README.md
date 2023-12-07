# Projet_Systeme2
Projet de système M1 S1
Analyseur de Variant

Ce programme compare les fichiers VCF issus de réplicats biologiques provenant d'un même échantillon afin d'identifier les variants communs entre ces réplicats. 
Ce test a une grande spécificité mais une faible sensibilité.


Ce projet contient trois fichiers principaux :

parcourir.py - Fichier Python pour parcourir le dossier en agument et stocker une liste des réplicats ainsi que leurs chemins.
compare.py - Fichier Python pour comparer les réplicats et déterminer les variants communs au sein d'un meme échantillon.
main.sh - Fichier bash pour exécuter le programme principal en utilisant le terminal.

Exécution du Programme
Pour exécuter ce programme sous un environnement Linux, utilisez le fichier bash main.sh dans le terminal avec la commande : 
1. ./main.sh ./cheminAbsoluDossierContenantLesFichiersAComparer
2. Pour trouver le chemin absolu il faut, avec le terminal, aller là ou se trouve le dossier (avec les commandes cd et ls). Puis faire la commande pwd, on récupère ce qui s'affiche. Pour finir il faut rajouter /NomDuDossierContenantLesFichiersAComparer à la fin.
3. Le programme accepte également l'option -h pour afficher l'aide. Pour afficher l'aide, exécutez :
./main.sh -h


Attention : 
1. Vos fichiers de réplicats doivent etres au format VCF (.vcf).
2. Avec un nom comme ceci : P+numéro_echantillon-numéro_réplicat.vcf.
3. Assurez-vous que le fichier ait les permissions d'exécution, sinon, utilisez la commande suivante pour donner la permission :
chmod +777 main.sh compare.py parcourir.py


Signification biologique des différences de similarité entre réplicats :

A. Moins de similarité entre réplicats :
  1. Une faible similarité peut indiquer des variations pouvant résulter de mutations aléatoires lors de l'amplification par exemple et donc une faible qualité des échantillons et des réplicats de ceux-ci.
  2. Conditions variables : Des environnements variables ou des traitements différents des échantillons peuvent conduire à des différences génétiques entre les réplicats.

B. Plus de similarité entre réplicats :
  1. Peut indiquer des conditions experimentales plus homogènes pour chaque réplicats.
  2. Peut indiquier une ou plusieurs véritables variations génétique par rapport au génome de référence (Vous pouvez donc écarter l'hypothèse d'une variation génétique due a une erreur de manupulation ou d'amplification).

Ces interprétations sont des pistes pour comprendre la signification biologique des résultats de comparaison entre réplicats, mais des analyses plus poussées et une intégration de données supplémentaires peuvent être nécessaires pour une interprétation complète.

Si vous avez des questions ou des difficultés pour utiliser le programme : emma.mathieu02@etu.umontpellier.fr

Merci d'avoir lu et utiliser ce programme.

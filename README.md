# Projet_Systeme2
Projet de système M1 S1
Nom du Programme
Description brève du programme et de son objectif principal.

Contenu du Projet
Ce projet contient trois fichiers :

parcourir.py - Fichier Python pour parcourir le dossier en agument et stocker une liste des réplicats ainsi que leurs chemins.
compare.py - Fichier Python pour comparer les réplicats et déterminer les variants communs au sein d'un meme échantillon.
main.sh - Fichier bash pour exécuter le programme principal en utilisant le terminal.

Exécution du Programme
Pour exécuter ce programme sous un environnement Linux, utilisez le fichier bash main.sh dans le terminal avec la commande : 
./main.sh NomDuDossierContenantLesFichiers

Assurez-vous que le fichier ait les permissions d'exécution, sinon, utilisez la commande suivante pour donner la permission :
chmod +777 main.sh compare.py parcourir.py

Le programme accepte également l'option -h pour afficher l'aide. Pour afficher l'aide, exécutez :
./main.sh -h


Fonctionnalités
Ce programme permet de :

Parcourir les fichiers de réplicats.
Comparer les réplicats et déterminer le nombre de variants communs entre les réplicats deux à deux au sein d'un échantillon.

Attention : 
Vos fichiers de réplicats doivent etres au format VCF (.vcf).
Avec un nom comme ceci : P+numéro_echantillon-numéro_réplicat.vcf.

Ce programe vous donneras le nombre de variants uniquement pour une insertion connue et commune entre chaque réplicats deux à deux. 

Merci d'avoir lu et utiliser ce programme.

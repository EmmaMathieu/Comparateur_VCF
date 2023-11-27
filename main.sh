#!/bin/bash
# C'est le shebang : le caractère "#!" veut dire que c'est une instruction système qui dit que c'est un script mais pas un fichier binaire, 
# Le /bin/bash est le répertoire d'execution pour bash ou la localisation de l'interpréteur permettant d'executer le script



echo -e "\nBienvenue dans ce programme qui analyse les variants génétiques.\nVous avez à disposition un dossier Data dans lequel vous pouvez mettre vos échantillons et vos réplicats au format VCF.\nAvec un nom comme ceci : P+numéro_echantillon-numéro_réplicat.vcf.\nCe programe vous donneras le nombre de variants uniquement pour une insertion connue et commune entre chaque réplicats deux à deux.\nSoit par :\n\t\t1) Position Identique.\n\t\t2) Position +/-10b.\n\t\t3) Avec une positon +/- 10b mais seulement lorsque les séquences se ressemblent à 75%.\n"
# -e pour echo permet l'interpretation par bash des chars {'\t' (permet une tabulation) et '\n' (permet de mettre a la ligne)} 

if [ $# -ne 1 ] || [ $1 = "-h" ]; then
    echo -e "\tUtilisation : \n\t\tVous avez donné le mauvais nombre d'arguments, veuillez mettre l'unique chemin après : $0"
    exit 1
fi
# Vérifie si un argument (chemin vers le dossier Data) est passé en ligne de commande
# Si le cardinal (#) des arguments ($) est différent de (-ne) 1, alors print ce qui est écrit
# Ou (||) si le premier argument est égal à "-h" alors afficher l'aide
# Le exit sert a sortir du programme et ne pas faire la suite du programme

racine="$1"

# Appel du script compare.py
python3 compare.py "$racine"

#python3 parcourir.py "$racine"
# Cree par Emma MATHIEU : https://github.com/EmmaMathieu
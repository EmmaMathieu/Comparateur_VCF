#!/bin/bash
# C'est le shebang : le caractère "#!" veut dire que c'est une instruction système qui dit que c'est un script mais pas un fichier binaire, 
# Le /bin/bash est le répertoire d'execution pour bash ou la localisation de l'interpréteur permettant d'executer le script



echo -e "\nBienvenue dans ce programme qui analyse les variants génétiques.\nCe programe vous donneras le nombre de variants uniquement pour une insertion connue et commune entre chaque réplicats deux à deux.\nSoit par :\n\t\t1) Positions et séquences identiques.\n\t\t2) Positions avec +/- 10 nucléotides de différences et séquences identiques.\n"

# -e pour echo permet l'interpretation par bash des chars {'\t' (permet une tabulation) et '\n' (permet de mettre a la ligne)} 

if [ $1 = "-h" ]; then # Vérifie si le premier argument est égal à "-h" alors afficher l'aide
    echo -e "\nVeuillez mettre le nom de l unique fichier contenant les fichier a comparer après : $0.\nVos fichiers de réplicats doivent etres au format VCF (.vcf) avec un nom comme ceci : P+numéro_echantillon-numéro_réplicat.vcf"
    exit 1 # Le exit sert a sortir du programme et ne pas faire la suite du programme
fi

if [ $# -ne 1 ] ; then # Si le cardinal (#) des arguments ($) est différent de (-ne) 1, alors print ce qui est écrit
    echo -e "\nVous avez donné le mauvais nombre d arguments, veuillez mettre le nom de l unique fichier contenant les fichier a comparer après : $0"
    exit 1
fi

racine="$1"

# Appel du script compare.py qui lui même appelera le script parcourir.py
python3 compare.py "$racine"

echo -e "\nPistes d interprétation : si un variant est compris dans tout les réplicats d un échantillon, il y a de fortes chances pour que ce variant provienne d une réelle mutation dans l échantillon. A l inverse, si une variation ne se trouve que dans un seul réplicat, il y a de fortes chances pour que cette mutation soit une erreur d'amplification fortuite.\n"
# Cree par Emma MATHIEU : https://github.com/EmmaMathieu
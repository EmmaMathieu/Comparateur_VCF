#!/bin/bash
# C'est le shebang : le caractère "#!" veut dire que c'est une instruction système qui dit que c'est un script mais pas un fichier binaire, 
# Le /bin/bash est le répertoire d'execution pour bash ou la localisation de l'interpréteur permettant d'executer le script
# -e pour echo permet l'interpretation par bash des chars {'\t' (permet une tabulation) et '\n' (permet de mettre a la ligne)} 

#S'il n'y a pas assez d'arguments
if [ $# -lt 1 ]; then # Si le cardinal (#) des arguments ($) est inferieur à 1 (c'est a dire deux arguments en langage humain), alors print ce qui est écrit
    echo -e "\nVous n'avez pas donné assez d'arguments\n"
    exit 1 # Le exit sert a sortir du programme et ne pas faire la suite du programme
fi

#S'il y a trop d'arguments
if [ $# -gt 3 ]; then # Si le cardinal (#) des arguments ($) est superieur à (-gt) 3, alors print ce qui est écrit
    echo -e "\nVous avez donné trop d arguments\n"
    exit 1
fi

# Vérifie si le premier argument est égal à "-h" alors afficher l'aide
#if [ $1 = "-h" ]; then 
    #echo -e "\nVeuillez mettre le chemin absolu de l unique dossier contenant les fichier à comparer après : $0.\nVos fichiers de réplicats doivent etres au format VCF (.vcf) avec un nom comme ceci : P+numéro_echantillon-numéro_réplicat.vcf\n"
    #exit 1 
#fi

# Vérifie si le premier argument est égal à "-h" pour afficher l'aide
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo -e "\nCe script compare les fichiers VCF dans un dossier spécifié pour analyser les variants communs entre les réplicats d'un échantillon.\nPour déterminer si les variants sont identiques, le programme prendra en compte :\n\n\t- la séquence et la position si la séquence de variation est spécifiée\n\t- Le type, la position et la longueur si la séquence de variation n'est pas spécifiée.\n"
    echo -e "Utilisation : $0 [chemin_dossier] [décalage_position] [pourcentage_identité]\n" 
    echo -e "Arguments :"
    echo -e "\t[chemin_dossier] :\t\tChemin absolu du dossier contenant les fichiers à comparer."
    echo -e "\t[décalage_position] :\t\tDécalage de position jusqu'auquel vous acceptez."
    echo -e "\t[pourcentage_identité] :\tPourcentage d'identité minimum accepté entre les séquences."
    echo -e "\nInformations : Les fichiers doivent être au format VCF (.vcf) avec un nom tel que P+numéro_echantillon-numéro_réplicat.vcf\n"
    exit 1 
fi

# Erreur si le dossier donné n'existe pas
if [ ! -d "$1" ];then
    echo -e "\nle dossier n'existe pas au chemin donné.\n"
    exit 2
fi

# Erreur s'il n'y a pas de fichier VCF dans le répertoire
if ! find "$1" -type f -name "*.vcf" -print -quit | grep -q .; then
    echo -e "\nle dossier ne contient pas de fichier avec l'extension VCF.\n"
    exit 3
fi

# Appel du script compare.py qui lui-même appelera le script parcourir.py en fonction du nombre d'arguments

# Vérifie si le nombre d'arguments passés est égal à 1
if [ $# -eq 1 ]; then
    # Si un seul argument est passé, appelle compare.py avec un seul argument ($1)
    python3 compare.py "$1"
fi

# Vérifie si le nombre d'arguments passés est égal à 2
if [ $# -eq 2 ]; then
    # Si deux arguments sont passés, appelle compare.py avec deux arguments ($1 et $2)
    python3 compare.py "$1" "$2"
fi

# Vérifie si le nombre d'arguments passés est égal à 3
if [ $# -eq 3 ]; then
    # Si trois arguments sont passés, appelle compare.py avec trois arguments ($1, $2 et $3)
    python3 compare.py "$1" "$2" "$3"
fi


# echo -e "\nPistes d interprétation : si un variant est compris dans tout les réplicats d un échantillon, il y a de fortes chances pour que ce variant provienne d une réelle mutation dans l échantillon. A l inverse, si une variation ne se trouve que dans un seul réplicat, il y a de fortes chances pour que cette mutation soit une erreur d'amplification fortuite.\n"
# Cree par Emma MATHIEU : https://github.com/EmmaMathieu
#!/bin/bash
# le caractère "#!" veut dire que c'est une instruction système, le /bin/bash est le répertoire d'execution pour bash

# Vérifie si un argument (chemin vers le dossier Data) est passé en ligne de commande
# Si le cardinal (#) des arguments ($) est différent de (-ne) 1, alors print ce qui est écrit
# Le exit sert a sortir du programme et ne pas faire la suite du programme
if [ $# -ne 1 ]; then
    echo "Vous avez donné le mauvais nombre d'arguments, veuillez mettre l'unique chemin après $0"
    exit
fi

racine="$1"

# Appel du script parcourir.py avec le chemin en argument
#python3 parcourir.py "$racine"

# Appel du script compare.py
python3 compare.py "$racine"
import sys
import parcourir
import matplotlib.pyplot as plt

plt.ion()

d = {'A':0, 'T':1, 'C':2, 'G':3}
matrice = [[2, -1, -1, 1],
           [-1, 2, 1, -1],
           [-1, 1, 2, -1],
           [1, -1, -1, 2]]
g = -10

def miseSousFormatDictionnaire(echantillon_et_replicats: dict) -> dict:
    """
    miseSousFormatDictionnaire(echantillon_et_replicats)
    \nEntree:
        Echantillon_et_replicats: Dictionnaire contenant les chemins des fichiers VCF pour chaque échantillon.
    \nSortie:
        Dictionnaire avec comme clé les différents passages et comme valeur :
            Dictionnaire avec comme clé les différents réplicats et comme valeur :
                Dictionnaire avec comme clé les différentes positions et comme valeur :
                    Liste de tuples contenant les informations sur les variants (Insertion, Deletion, Duplication), et leur fréquence.
    \nExemple sortie:
        {'P15': 
            {'P15-1': {'1': [('A', 1, 1, 0.1), ('T', 1, 1, 0.2)], '2': [('C', 1, 1, 0.3)]}, 
             'P15-2': {'1': [('A', 1, 1, 0.1), ('T', 1, 1, 0.2)]} }, 
        'P30': 
            {'P30-1': {'1': [('A', 1, 1, 0.1), ('T', 1, 1, 0.2)]} }
        }

    """
    dictionnaire_passage = {}

    # Crée un dictionnaire pour chaque échantillon.
    for echantillon, chemins_rep in echantillon_et_replicats.items():
        dictionnaire_echantillon = {}

        # Pour chaque réplicat, il crée un nouveau dictionnaire.
        for chemin_r in chemins_rep:
            dictionnaire_position = {}
            nom_fichier = chemin_r.split('/')[-1]  # Récupère le nom du fichier à partir du chemin complet.

            with open(chemin_r, 'r') as f:
                for ligne in f:
                    if ligne.startswith('#'):
                        continue
                    colonne = ligne.split('\t')
                    valeur_colonne_1, valeur_colonne_4, valeur_colonne_7, valeur_colonne_9 = int(colonne[1]), colonne[4], colonne[7], colonne[9]

                    freq = valeur_colonne_7.split('AF=')[1].split(';')[0] if 'AF=' in valeur_colonne_7 else None
                    prof = int(valeur_colonne_9.split(':')[2]) + int(valeur_colonne_9.split(':')[3])

                    svlen = valeur_colonne_7.split('SVLEN=')[1].split(';')[0] if 'SVLEN=' in valeur_colonne_7 else None

                    
                    # Si la position du variant n'est pas déjà présente, crée une nouvelle entrée dans le dictionnaire.
                    if valeur_colonne_1 not in dictionnaire_position:
                        dictionnaire_position[valeur_colonne_1] = []

                    # On ajoute la séquence, la taille, la fréquence et la profondeur de chaque variant avec comme clé la position.
                    dictionnaire_position[valeur_colonne_1].append([valeur_colonne_4, int(svlen), float(freq), prof])

            # Associe les valeurs des colonnes 1 et 4 au nom du fichier.
            if dictionnaire_position:
                dictionnaire_echantillon[nom_fichier] = dictionnaire_position

        # Modification des clés du dictionnaire final pour enlever les informations supplémentaires et rendre la sortie plus visible
        dictionnaire_echantillon_modifie = {}
        for cle, valeur in dictionnaire_echantillon.items():
            nouvelle_cle = cle.split('.')[0] if '.' in cle else cle
            dictionnaire_echantillon_modifie[nouvelle_cle] = valeur

        if dictionnaire_echantillon_modifie:
            dictionnaire_passage[echantillon] = dictionnaire_echantillon_modifie
    return dictionnaire_passage


def verifseq(seq, taille) :
    if seq == "<INS>" or seq == "<DEL>" or seq == "<DUP>" :
        return seq, abs(taille) % 3
    elif type(seq) is str :
        taillemaxrep = int(len(seq)/2)
        repe = seq
        nb = 1
        for i in range(1, taillemaxrep) :
            rep = seq[0:i]
            nbrep = seq.count(rep)
            taillerep = len(rep) * nbrep
            if len(seq) == taillerep :
                if i == 1 :
                    repe = rep
                    nb = nbrep
                elif i >= 2 :
                    repe = rep
                    nb = nbrep
                    break
            elif len(seq) * 0.75 <= taillerep :
                repe = rep
                nb = nbrep
                break
        testmodulo = len(repe) * nb
        testmodulo = testmodulo % 3
        return repe, testmodulo
        


def interrogff(position) :
	fichier = open("sequence.gff3","r")
	lignes = fichier.readlines()
	i = 1
	position = int(position)
	liste = []
	for l in lignes :
		if l[0] != "#":
			if len(l) > 1 :
				coord=l.split("\t")
				region=coord[2]
			if region == "gene" :
				deb=int(coord[3])
				fi=int(coord[4])
				etape1=coord[8]
				etape1=etape1.split(";")
				etape2=etape1[0]
				etape2=etape2.split("=")
				typ=etape2[1]
				if ":" in typ :
					typ=typ.split(":")
					typ=typ[0]
				if position >= deb and position <= fi:
					liste.extend([typ, deb, fi])
					break
		i+=1
	fichier.close()
	return liste

def test(variants, valeur):
    """
    test(variants, valeur)
    \nEntree:
        variants: Sequence du variant
        valeur: Sequence du variant
    \nSortie:
        True si les deux sequences sont similaires, False sinon
    \nExemple:
        test("ATG", "ATG") -> True
        test("ATG", "ATC") -> False
        test("<INS>", "ATG") -> True
        test("<DEL>", "<DUP>") -> False
    """
    if ((variants=="<INS>" or variants != "N") and (valeur=="<INS>" or valeur != "N")):
         return True
    elif ((variants=="<DEL>" or variants == "N") and ( valeur=="<DEL>" or valeur == "N")):
         return True
    elif (variants=="<DUP>" and valeur=="<DUP>"):
            return True
    return False

def mainAlignement(seq1, seq2):
    if (seq1=="<INS>" or seq2=="<INS>" or seq1=="<DEL>" or seq2=="<DEL>" or seq1=="<DUP>" or seq2=="<DUP>" or seq1=="N" or seq2=="N"):
        return True
    matriceScore = [[0 for i in range(len(seq2)+1)] for j in range(len(seq1)+1)]
    n = len(seq1)
    m = len(seq2)
    for i in range(1,n+1):
        matriceScore[i][0] = matriceScore[i-1][0] + g
    for j in range(1,m+1):
        matriceScore[0][j] = matriceScore[0][j-1] + g
    for i in range(1,n+1):
        for j in range(1,m+1):
            matriceScore[i][j] = max(matriceScore[i-1][j-1] + matrice[d[seq1[i-1]]][d[seq2[j-1]]],matriceScore[i-1][j] + g,matriceScore[i][j-1] + g)
    maxi = min(len(seq1), len(seq2))*2 + g*(abs(len(seq1)-len(seq2)))
    mini = (len(seq1) + len(seq2))*g
    diff = (maxi - mini) * 0.25
    if matriceScore[n][m] >= maxi - diff:
        return True
    return False

def add(ch1, ch2):
    return ch1 + ch2

def moy(ch1, ch2):
    return (ch1 + ch2) / 2

def assemblageDeVariants(dico, decalage, op=add) -> dict:
    for value_passage in dico.values():
        for replicat, value_replicat in value_passage.items():
            dictionnaire_replicat = dict()
            l_variants = list()
            for position, variants in value_replicat.items():
                gff=interrogff(position)
                # print(gff)
                for variant in variants:
                    if(op==add):
                        if (len(gff) == 3):
                            variant.extend(gff)
                        else:
                            variant.extend([None,None,None])
                    l_variants.append((position, variant))
            # print(l_variants)

            for d in range(0, decalage+1):
                i = 0
                while i < len(l_variants):
                    position, variant = l_variants[i]
                    j = i+1
                    while j < len(l_variants):
                        position2, variant2 = l_variants[j]

                        if position2 - position == d:
                            if(test(variant[0], variant2[0]) and mainAlignement(variant[0], variant2[0])):
                                l_variants[i] = (position, [variant[0], variant[1], min(round(op(variant[2],variant2[2]),4),1.0),  op(variant[3],variant2[3]), variant[4], variant[5], variant[6]]) 
                                l_variants.pop(j)
                                continue
                        if position2 - position > d:
                            break
                        j += 1
                    i += 1

            # print(l_variants)
            
            for pos, var in l_variants:
                if pos in dictionnaire_replicat:
                    dictionnaire_replicat[pos].append(var)
                else:
                    dictionnaire_replicat[pos] = [var]
            value_passage[replicat] = dictionnaire_replicat
    return dico

def filtre_dico(dico, pourcentage=0.1):
    """
    filtre_dico(dico)
    \nEntree:
        dico: Dictionnaire contenant les variants.
    \nSortie:
        dictionnaire filtré pour ne garder que les variants avec une fréquence supérieure à 10%.
    \nExemple:
        Entree:
            {'P15':
                {'P15-1': {'1': [('A', 1, 1, 0.1), ('T', 1, 1, 0.2)], '2': [('C', 1, 1, 0.3)]}, 
                'P15-2': {'1': [('A', 1, 1, 0.1), ('A', 1, 1, 0.2)]} }
            }
        Sortie:
            {'P15':
                {'P15-1': {'1': [('T', 1, 1, 0.2)], '2': [('C', 1, 1, 0.3)]}, 
                'P15-2': {'1': [('A', 1, 1, 0.2)]} }
            }
    """
    for valeurs_passage in dico.values():
        for keys_replicat, valeurs_replicat in valeurs_passage.items():
            dico_tmp = {}
            for clef, valeurs in valeurs_replicat.items():
                nouveaux_tuples = []

                for valeur in valeurs:
                    if valeur[2] > pourcentage:
                        nouveaux_tuples.append(valeur)
                    
                if nouveaux_tuples:
                    dico_tmp[clef] = nouveaux_tuples
        valeurs_passage[keys_replicat] = dico_tmp      
    return dico


def infovariants(dico, name="InfoVariants.txt"):
    with open(name, 'w') as fichier:
        for passage, value_passage in dico.items():
            fichier.write("- Passage " + str(passage) + " :\n\n")
            comp = 0
            for replicat, value_replicat in value_passage.items():
                tmp = 0
                for variants in value_replicat.values():
                    for variant in variants:
                        tmp += 1
                fichier.write("Replicat " + str(replicat) + " a " + str(tmp) + " variantions\n")
                comp += tmp
            fichier.write("\nIl y a " + str(comp) + " variantions en tout\n")
            fichier.write("La moyenne est de " + str(comp/len(dico[passage].keys())) + " variantions par replicat\n\n\n")

def ecrireVariants(dico, name="Variants.txt"):
    with open(name, 'w') as fichier:
        fichier.write("Passage;Replicat;Position;Variants;Taille;Frequence;Profondeur;Gene;DebG;FinG\n")
        for passage, value_passage in dico.items():
            for replicat, value_replicat in value_passage.items():
                for position, variants in value_replicat.items():
                    for variant in variants:
                        fichier.write(str(passage) + ";" + str(replicat) + ";" + str(position) + ";")
                        for i in range(len(variant)):
                            if(i != len(variant)-1):
                                fichier.write(str(variant[i]) + ";")
                                continue
                            fichier.write(str(variant[i]))
                        fichier.write("\n")
                        if(variant[2]>1.0):
                            Warning("Attention, la fréquence est supérieure à 1" + str(variant) + str(position) + str(replicat) + str(passage))

def pool(dico):
    resultat = {}
    for passage, value_passage in dico.items():
        d = {}
        l = []
        for replicat, value_replicat in value_passage.items():
            for position, variants in value_replicat.items():
                for variant in variants:
                    l.append((position, variant))
        
        l.sort()
        for pos, var in l:
            if passage in d:
                if pos in d[passage]:
                    d[passage][pos].append(var)
                else:
                    d[passage][pos] = [var]
            else:
                d[passage] = {pos: [var]}
        resultat[passage] = d
    return resultat

def mise_en_forme(comparaisons: dict, str) -> str:
    resultat = "\n" + str + "\n"
    resultat += "\n-----------------------Premier echantillon-----------------------\n"
    cles = list(comparaisons.keys())

    for i, cle in enumerate(cles):
        resultat += f"le couple de réplicat : {cle} a un nombre de variant commun égal à : {comparaisons[cle]}\n"
        premier_tiret_cle = cle.index('-') if '-' in cle else len(cle)
        
        if i < len(cles) - 1 and cle[:premier_tiret_cle] != cles[i + 1][:premier_tiret_cle]:
            resultat += "\n-----------------------Echantillon suivant-----------------------\n"
    return resultat

def ecrire_dans_fichier(chemin_sortie: str, resultat_concatene: str):
    with open(chemin_sortie, 'w') as fichier:
        fichier.write(resultat_concatene)


def printDico(dico):
    for cle, valeur in dico.items():
        print(cle, ":")
        for cle2, valeur2 in valeur.items():
            print(cle2, ":")
            for cle3, valeur3 in valeur2.items():
                print("\t", cle3, ":", valeur3)
            
def printTitle(phrase):
    taille = 75
    print("\n")
    print("#"*taille)
    print(phrase.center(taille))
    print("#"*taille)


def main():
    # DEBUG (Affichage des dictionnaires intermédiaires)
    debug = False


    # Recuperation du chemin contenant les fichiers VCF a analyser
    chemin = sys.argv[1]
    #chemin = "PALL/"

    if len(sys.argv) == 4: 
        # Prend les arguments 2 et 3 comme décalage et pourcentage
        decalage = int(sys.argv[2]) 
        pourcentage = int(sys.argv[3])
    elif len(sys.argv) == 3:
        # Initialisation du décalage avec l'agruement 2 et du pourcentage de similarité à 100%
        decalage = int(sys.argv[2])
        pourcentage = 100 
    else: 
        # Initialisation de tout les arguments par defaut.
        # Pas de décalage, 100% de similarité
        decalage = 0
        pourcentage = 100 


    phrase = "Bienvenue dans ce programme qui analyse le nombre de variants communs entre chaque réplicats deux à deux au sein d'un échantillon.\nLes paramètres sont les suivants :\n\n\tPourcentage de similarité minimum entre les séquences communes : " + str(pourcentage) + "\n\tDécalage d'alignement maximum entre les variants (shift) : " + str(decalage)
    print(phrase)
    
    echantillon_et_replicats = parcourir.parc(chemin)    

    # Premiere etape, mise sous forme de dictionnaire
    dictionnaire_de_variants = miseSousFormatDictionnaire(echantillon_et_replicats)

    if(debug):
        printTitle("Dictionnaire de base")
        printDico(dictionnaire_de_variants)

    # Deuxieme etape, on assemble les variants qu'on considère comme similaires        
    dictionnaire_avec_variants_assemble_par_proximite = assemblageDeVariants(dictionnaire_de_variants, decalage)

    if(debug):
        printTitle("Apres assemblage")
        printDico(dictionnaire_avec_variants_assemble_par_proximite)

    # Troisieme etape, on filtre les variants pour ne garder que ceux qui ont une fréquence supérieure à 10%
    for nb in range(0,10):
        dictionnaire_final = filtre_dico(dictionnaire_avec_variants_assemble_par_proximite, nb/10)
        infovariants(dictionnaire_final, "Resultats/InfoVariants/InfoVariants_" + str(nb/10) + ".txt")
        ecrireVariants(dictionnaire_final, "Resultats/Variants/Variants_" + str(nb/10) + ".txt")

    if(debug):
        printTitle("Apres filtre")
        printDico(dictionnaire_final)

    
    p = pool(dictionnaire_final)
    p2 = assemblageDeVariants(p, decalage, moy)

    infovariants(p2, "la.txt")
    ecrireVariants(p2, "le.txt")

    if(0):
        variant = []
        frequences = []
        zones = []
        d = {}
        for value_passage in p2.values():
            for value_replicat in value_passage.values():
                for position, variants in value_replicat.items():
                    for v in variants:
                        variant.append(position)
                        frequences.append(v[2])
                        if (v[4] not in d):
                            zones.append((v[4], v[5], v[6]))
                            d[v[4]] = 1
        
        plt.figure(figsize=(10, 6))
        plt.bar(variant, frequences, width=2500 , color='blue', align='center', label='Fréquence')
        
        for (gene, start, end) in zones:
            plt.axvspan(start, end, color='red', alpha=0.3, label=gene)

        plt.xlabel('Position des variants')
        plt.ylabel('Fréquence')
        plt.title('Fréquence des variants et zones représentant les gènes')
        # plt.legend()

        plt.show()
        # plt.waitforbuttonpress()
        input()


if __name__ == "__main__":
    # Si le fichier est exécuté en tant que programme principal, appelle la fonction main
    main()



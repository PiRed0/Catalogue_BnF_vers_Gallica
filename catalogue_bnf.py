##############################################################
### Web scraper pour des liens de numérisation sur Gallica ###
##############################################################




## Packages nécessaires au déroulement du programme
import re
import urllib.request as url_req
from bs4 import BeautifulSoup as bs




## Ensemble des fonctions nécessaires à l'exécution du programme
def langue(seq: str, sep: str) -> list[str]:
    """Précondition : len(c) = 1
    Retourne une liste de langues à partir d'une chaîne de caractères listant les langues
    avec un caractère unique et spécifique pour séparer les langues.
    """

    LR: list[str] = []  # Liste résultat
    t: str = ''  # Séquence temporaire de stockage des langues

    e: str  # Elément de parcours
    for e in seq:
        if e != sep:
            t = t + e
        else:
            LR.append(t)
            t = ''
    if t != '':
        LR.append(t)

    return LR


# Jeu de tests
assert langue('latin.francais.anglais', '.') == ['latin', 'francais', 'anglais']
assert langue('', ' ') == []
assert langue('ethiopien norrois arabe', ' ') == ['ethiopien', 'norrois', 'arabe']


def regex_cote(LL: list[str]) -> list[str]:
    """Retourne une liste d'expressions régulières (chaînes de caractères) pour chaque langue de la liste LL.
    """

    LR: list[str] = []  # Liste résultat
    t: str = ''  # Séquence temporaire de stockage des langues

    e: str  # Elément de parcours
    for e in LL:
        t = e + '\+\d+'
        LR.append(t)

    return LR


# Jeu de tests
assert regex_cote(['latin', 'francais', 'anglais']) == ['latin\+\d+', 'francais\+\d+', 'anglais\+\d+']
assert regex_cote([]) == []


def extraction_cotes(LRe: list[str], fichier: str) -> list[str]:
    """Précondition : LRe contient des RegEx (Expressions régulières)
    Précondition : fichier correspond à un chemin et un document au format .txt (ex : "C:/documents/mon_fichier.txt")
    Retourne une liste de cotes de manuscrits trouvées dans un fichier .txt à partir d'une liste de RegEx.
    """

    corpus = open(fichier, 'r+').read()
    LR: list[str] = []

    e: str # élément de parcours
    for e in LRe:
        LR = LR + re.findall(e, corpus)

    return LR


# Aucun test chemin dépend de la machine de l'utilisateur



def ecriture_sortie(LC: list[str], fichier: str) -> None:
    """Précondition : le fichier en entrée est au format .txt
    Précondition : le fichier en sortie est au format .txt
    Précondition : les cotes sont renseingées dans le fichier en entrée selon la forme 'langue+numéro' (ex : latin+154)

    Retourne dans un fichier .txt une liste d'URL de documents de la BnF numérisés ou non sur Gallica
    à partir d'une liste de cotes dans un fichier .txt.
    """

    fichier_sortie = open(fichier, 'w')

    url_base = 'https://archivesetmanuscrits.bnf.fr/'
    url_part1 = 'resultatRechercheSimple.html?TEXTE_LIBRE_INPUT='
    url_part2 = '&FACET_TROUVE_DANS_SELECTED=COTE_INPUT&COTE_INPUT='

    e: str # élément de parcours
    for e in LC:

        url_recherche: str = url_base + url_part1 + e + url_part2 + e
        recherche_catalogue = url_req.urlopen(url_recherche)
        soupe_recherche_catalogue = bs(recherche_catalogue)

        lien_notice = soupe_recherche_catalogue.find('a', title='Consulter ce résultat')

        if lien_notice:

            lien = lien_notice['href']
            url_notice: str = url_base + lien
            notice = url_req.urlopen(url_notice)
            soupe_num = bs(notice)

            num = soupe_num.find('a', title='Voir le document numérisé')

            if num:

                fichier_sortie.write(e + " : " + str(num['href']) + "\n")

            else:

                fichier_sortie.write(e + " : " + "aucun lien vers une numérisation" + "\n")

        else:

            fichier_sortie.write(e + " : " + "aucun lien vers une notice" + "\n")

    return None

# La fonction 'ecriture_sortie' n'est pas testée car elle renvoie un type 'None'.




## Déroulement du programme
langues_recherchees = input('Entrez une liste de cotes avec un séparateur unique.')
separateur = input('Entrez le caractère qui a servi de sépérateur précédemment.')

fichier_entree = input('Entrez le chemin du fichier en entrée.')
fichier_sortie = input('Entrez le chemin du fichier en sortie.')

liste_langue: list[str] = langue(langues_recherchees, separateur)
re_langues: list[str] = regex_cote(liste_langue)
liste_cotes: list[str] = extraction_cotes(re_langues, fichier_entree)
ecriture_sortie(liste_cotes, fichier_sortie)

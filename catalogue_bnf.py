from bs4 import BeautifulSoup as bs
import urllib.request as urlReq
import re

############################################################################################################################################
#### NB : Les cotes des manuscrits doivent être entrées sous la forme suivante: "langue+numéro" dans le fichier .csv ou .txt en entrée. ####
#### Exemple : latin+6964                                                                                                               ####
#### NB' : Pour les manuscrits français, il faut écrire "francais", sans la cédille dans votre fichier.                                 ####
############################################################################################################################################


fichierCorpus = input("Entrez le chemin et le nom du fichier où sont stockés les cotes des documents qui vous intérssent (sous la forme : \"C:/Users/nomUtilisateur/Emplacement/Dossier/nomFichier.txt\").")
fichierSortie = input("Entrez le chemin où vous souhaitez enregistrer le fichier qui sera créé avec les liens vers les numérisations, ainsi que le nom de ce nouveau fichier (sous la forme : \"C:/Users/nomUtilisateur/Emplacement/Dosseir/nomFichier.txt\").")

corpus = open(fichierCorpus, "r+").read() # Ouverture et lecture du fichier source, à partir de la saisie de l'utilisateur, dans lequel on va chercher les cotes des documents pour lesquels on souhaite connaître s'il existe une numérisation.
listeLiensNumerisations = open(fichierSortie, "w") # Définition, à partir de la saisie de l'utilisateur, du fichier de sortie dans lequel les liens de numérisation seront renseignés.


langue = ""
listeLanguesFonds = []


# Boucle permettant d'entrer manuellement les langues définissant les fonds concernés par la recherche de lien vers une numérisation des documents, jusqu'à la saisie de "FIN". #
while langue != "FIN":
    langue = input("Entrez les langues des fonds dans lesquels vous cherchez des manuscrits(francais - attention sans la cédille -, latin, arabe, etc.). Entrez : \"FIN\", pour terminer la saisie.")
    if langue != "FIN":
        listeLanguesFonds.append(langue) # Ajout de l'ensemble des langues saisies dans une liste.
    else:
        print(listeLanguesFonds) # Elément de contrôle, permettant à l'utilisateur de voir la liste des langues qu'il a entré et ainsi de pouvoir relancer le programme après, en cas de faute de frappe qui sera ainsi rapidement identifiée.


## MACRO-BOUCLE : permet pour chaque langue entrée de récupérer les cotes dans le fichier source, de construire les URL de recherche, d'accéder à la notice du document et de récupérer l'URL de la numérisation de ce dernier, si elle existe. Sinon le programme renvoie qu'il n'existe pas de numérisation. Si un problème s'est produit le programme peut renvoyer un message signifiant qu'il n'a pas trouvé la notice et ainsi renseigner l'utilisateur sur la nature du problème. ##
# Boucle permettant de construire l'expression régulière (ou les expressions) qui vont permettre de récupérer les cotes dans manuscrits dans le fichier source. #
for chaqueLangue in listeLanguesFonds:
    RegExCote = chaqueLangue + "\+\d+"
    coteBNF = re.finditer(RegExCote, corpus)
    # Boucle permettant de reconstituer les URL de recherche (spécifique à la cote) et de trouver dans la page web l'emplacement du potentiel lien vers la page web de la notice du document. #
    for chaqueCoteBNF in coteBNF:
        coteCible = chaqueCoteBNF.group(0)
        print(coteCible) # Elément de contrôle pour que l'utilisateur puisse voir en temps réel les cotes trouvées dans le fichier source par le programme.
        BaseURL = "https://archivesetmanuscrits.bnf.fr/" # Base de l'URL qui sert à la fois pour la page web de la recherche et dans celle de la notice.
        partie1url = "resultatRechercheSimple.html?TEXTE_LIBRE_INPUT=" # Partie invariable de l'URL de la page web de la recherche.
        partie2url = "&FACET_TROUVE_DANS_SELECTED=COTE_INPUT&COTE_INPUT=" # Partie invariable de l'URL de la page web de la recherche.
        urlRecherche = BaseURL + partie1url + coteCible + partie2url + coteCible # Constitution de l'URL de recherche à partir de la partie de base du site web, des parties invariables des pages de recherches et des cotes (parties variables des URL).
        print(urlRecherche) # Elément de contrôle qui affiche les URL des notices en temps réel, permettant à l'utilisateur de vérifier simplement le bon fonctionnement des URL construites par le programme.
        lienRecherche = urlReq.urlopen(urlRecherche)
        soupeCote = bs(lienRecherche)
        resultatRecherche = soupeCote.find("a", title="Consulter ce résultat")
        # Boucle permettant de trouver le lien de la page web de la notice du document (retour d'un message d'erreur dans le fichier de sortie quand cette page n'a pas été trouvée pour éviter une erreur qui arrêterait l'exécution du programme) et de trouver l'emplacement du potentiel lien vers une numérisation du document. #
        if resultatRecherche:
            LienRelatifNotice = resultatRecherche["href"]
            urlNotice = BaseURL + LienRelatifNotice
            LienNotice = urlReq.urlopen(urlNotice)
            soupeNotice = bs(LienNotice)
            resultatNumerisation = soupeNotice.find("a", title="Voir le document numérisé")
            # Boucle permettant d'accéder à l'URL de la numérisation du document, si elle existe, et qui l'inscrit dans le fichier de sortie. Si elle n'existe pas, le programme inscrit qu'il n'existe pas de numérisation disponible du document. #
            if resultatNumerisation:
                LienNumerisation = resultatNumerisation["href"]
                listeLiensNumerisations.write(str(coteCible) + " : " + str(LienNumerisation) + "\n") # L'enregistrement dans le fichier de sortie précise à chaque fois la cote du document avant le lien vers sa numérisation, ou l'un des deux messages d'erreur possible.
            else:
                listeLiensNumerisations.write(str(coteCible) + " : " + "aucun lien vers une numérisation" + "\n")
        else:
            listeLiensNumerisations.write(str(coteCible) + " : " + "aucun lien vers une notice" + "\n")

# RecuperationLiensGallica
Script Python pour récupérer à partir d'une liste de cotes de manuscrits de la BnF, leur lien de numérisation sur Gallica.

Python script to scrap manuscripts inventory of the BnF and collect their Gallica's numerisation link.

Le programme fonctionne de la manière suivante : il suffit de lui donner un fichier .txt dans lequel les cotes de manuscrits sont référencées selon ce modèle : "fonds+numéro" (ex : latin+16210, NAL+693, francais+158, etc.).
Le programme retourne la liste des cotes des manuscrits avec le lien de leur numérisation sur Gallica (URL : gallica.bnf.fr) s'ils existent, sinon il spécifie si l'absence de lien est dû à une erreur d'exécution ou s'il n'y a pas de lien existant.

This Python program works with a .txt file in input. In that file the syntax of bookmarks of the BnF's manuscripts has to follow this form: "collection+number" (ex: latin+16210, NAL+693, francais+158, etc.).
In output, the program returns, in a .txt file, a list of manuscripts' bookmarks in front of their numerisation link in Gallica (URL : gallica.bnf.fr), if they exist. Otherwise, the program specifies if the lack of link is due to an error during program's execution or if it's there is no numerisation.

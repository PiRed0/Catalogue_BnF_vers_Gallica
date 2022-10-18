# Catalogue_BnF_vers_Gallica
Script Python pour récupérer à partir d'une liste de cotes de manuscrits de la BnF, leur lien de numérisation sur Gallica.

Le programme fonctionne de la manière suivante : il suffit de lui donner un fichier .txt dans lequel les cotes de manuscrits sont référencées selon ce modèle : "fond+numéro" (ex : latin+16210, NAL+693, francais+158, etc.).
Le programme retourne la liste des cotes des manuscrits avec le lien de leur numérisation sur Gallica (URL : gallica.bnf.fr) s'ils existent, sinon il spécifie si l'absence de lien est dû à une erreur d'exécution ou s'il n'y a pas de lien existant.

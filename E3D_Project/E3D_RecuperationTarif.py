##
#   \file E3D_RecuperationTarif.py
#   \brief Fichier RecuperationTarif
#
#   Récupération des tarifs actuel dans la base MYSQL
#
#
#   \class RecuperationTarif
#   \brief Classe RecuperationTarif.
#
#   Permet de gérer la récupération des tarifs actuel de l'électricité dans la base de données MYSQL
#   \author Awen Ruaud
#   \version 1
#   \date  19 Mai 2021
#
import mysql.connector
from mysql.connector import errorcode
import json

class RecuperationTarif:    

    ## Constructeur
	#  \brief Constructeur de la Classe
    def __init__(self, tarifHC, tarifHP):
        # Ouverture du fichier de configuration 
        configuration = open("E3D_Project/config_Mysql.json","r")
        # Lecture du fichier de configuration 
        self.data = json.load(configuration)
        # Fermeture du fichier de configuration
        configuration.close() 
        self.tarifHC = tarifHC
        self.tarifHP = tarifHP

    ##
	#   Connexion à la base de données Mysql
	#
	# 	\brief Connexion Mysql.
	#
	#   - Initialise la connexion avec la base de données MYSQL
    #
    def connexionBaseTarif(self):
        # Connection à la base de données
        self.cnx = mysql.connector.connect(host=self.data["hote"],
                                         database=self.data["bdd"],
                                         user=self.data["utilisateur"],
                                         password=self.data["mdp"])
        self.cnx.autocommit = True
        # Création du curseur pour la lecture des données 
        self.cursor = self.cnx.cursor()

    ##
	#   Envoie de la requête à la base de données Mysql
	#
	# 	\brief Requête Mysql.
	#
	#   - Envoie une requête à la base de données MYSQL afin de récupérer le tarif voulu
    #
    def recupererTarif(self):
        # Envoie des requêtes
        # Premier requête : Prix du kWh Heure Creuse
        self.tarifHC = self.cursor.execute("SELECT `montant_tarif` FROM `tarif` WHERE `id_ressource`= 2 AND CURRENT_DATE BETWEEN `debut_tarif` AND `fin_tarif`")
        # Recherche de la données dans le curseur
        for (montant_tarif) in self.cursor:
            self.tarifHC = montant_tarif
        # Premier requête : Prix du kWh Heure pleine
        self.tarifHP = self.cursor.execute("SELECT `montant_tarif` FROM `tarif` WHERE `id_ressource`= 3 AND CURRENT_DATE BETWEEN `debut_tarif` AND `fin_tarif`")
        # Recherche de la données dans le curseur
        for (montant_tarif) in self.cursor:
            self.tarifHP = montant_tarif
        # Fermeture de la connexion avec la base de données
        self.cnx.close()

    ## Récuperer tarif
	#  \brief Récupère le tarif Heure creuse actuel 
    def get_tarif_HC(self):
        return self.tarifHC

    ## Récuperer tarif
	#  \brief Récupère le tarif Heure pleine actuel 
    def get_tarif_HP(self):
        return self.tarifHP


if __name__ == "__main__":
    tarif_hc = 0
    tarif_hp = 0
    # Création de l'objet RecuperationTarif
    a = RecuperationTarif(0, 0)
    try:
        # Essaie de la connexion
        a.connexionBaseTarif()
    except mysql.connector.Error as err:
        # Si la connexion ne fonctionne pas, écrire les erreurs
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        # Connection réussie, appelle des méthodes
        a.recupererTarif()
        tarif_hc = a.get_tarif_HC()
        tarif_hp = a.get_tarif_HP()
        print(tarif_hc[0])
        print(tarif_hp[0])
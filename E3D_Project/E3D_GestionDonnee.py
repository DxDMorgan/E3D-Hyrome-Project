##
#   \file E3D_GestionDonnee.py
#   \brief Fichier E3D_GestionDonnee 
#
#   Traitement des données à des fins d'insertion dans Influxdb
#
#
#   \class GestionDonnee
#   \brief Classe GestionDonnee.
#
#   Permet de gérer l'association du métrique avec le Prix du kWh (heure creuse + heure pleine), l'insertion de la donnée ainsi créée dans une base influxdb
#   \author Awen Ruaud
#   \version 1
#   \date  28 Mai 2021
#
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json

class GestionDonnee:

     ## Constructeur
	#  \brief Constructeur de la Classe
    def __init__(self, tarifHC, tarifHP, metrique):
        # Ouverture du fichier de configuration 
        configuration = open("E3D_Project/config_Influxdb.json","r")
        # Lecture du fichier de configuration 
        self.data = json.load(configuration)
        # Fermeture du fichier de configuration
        configuration.close()
        self.tarifHC = tarifHC
        self.tarifHP = tarifHP
        self.metrique = metrique

    ##
	#   Connexion à la base de données Influxdb
	#
	# 	\brief Connexion Influxdb.
	#
	#   - Initialise la connexion avec la base de données Influxdb
    #
    def connexionBaseMetrique(self):
        # Définition des paramètre de connexion du client influxdb
        self.client = InfluxDBClient(url=self.data["url"], 
                                     token=self.data["token"], 
                                     org=self.data["org"])
        # Définition de la methode d'écriture du client influxdb
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
    
    ##
	#   Association du métriques avec le tarif
	#
	# 	\brief Association Métrique tarif.
	#
	#   - Associe le métrique avec le dernier tarif recupéré
    #
    def associerMetriqueTarif(self):
        # Association du métrique avec les prix du kWh en une donnée
        self._data1 = Point("Modbus_data_test").field("Prix du kWh HC", self.tarifHC).field("Prix du kWh HP", self.tarifHP).field("consomation WH", self.metrique)
    
    ##
	#   Écriture des données dans la base influxdb 
	#
	# 	\brief Envoie des données.
	#
	#   - Écrit les données (tarif et métrique) dans la base influxdb
    #
    def envoieDonnées(self):
        # Ecriture de la donnée précédemment créée dans la base Influxdb 
        self.write_api.write(bucket="Consommation_Modbus", record=[self._data1])


if __name__ == "__main__":
    tarif_hc = 0.8
    tarif_hp = 1.3
    metrique = 65586137593
    # Création de l'objet
    a = GestionDonnee(tarif_hc, tarif_hp, metrique)
    # Appel des fonctions
    a.connexionBaseMetrique()
    a.associerMetriqueTarif()
    a.envoieDonnées()
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
#   \version 2
#   \date  28 Mai 2021
#
import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import errorcode
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import time

class GestionMQTT:
    ## Constructeur
	#  \brief Constructeur de la Classe
    def __init__(self, controleur):
        # Appel de la classe controleur
        self.controleur = controleur
        # Appel de la methode "recuperationMQTT"
        self.recuperationMQTT()

    ##
	#   Connexion MQTT
	#
	# 	\brief Connexion au broker.
	#
	#   - Inialisation de la connexion au broker MQTT
    #
    def recuperationMQTT(self):
        # Création d'un client MQTT
        self.mqttclient = mqtt.Client()
        self.mqttclient.on_connect = self.on_connect
        self.mqttclient.on_message = self.on_message
        # Connexion au broker MQTT
        self.mqttclient.connect("51.254.200.114", 1883, 60)
        
    ##
	#   Subscribe MQTT
	#
	# 	\brief Aquisition du topic.
	#
	#   - Inialisation de l'abonnement au topic à partir du moment où le client reçoit une confirmation de connexion du broker
    #
    def on_connect(self, client, userdata, flags, rc):
        # Debug pour vérifier que la connexion est bien établie
        print("Connected with result code "+str(rc))
        # L'abonnement se trouve dans "on_connect", ce qui signifie que, 
        # en cas de reconnexion l'abonnement sera renouvelé automatiquemen
        # Récupération du topic contenant l'indice du compteur
        self.mqttclient.subscribe("Enerium/Modbus1/indice/#")

    ##
	#   Récupération MQTT
	#
	# 	\brief Récupération du topic.
	#
	#   - Dès qu'un message est reçu, le topic est traité afin de ne recupérer que l'indice Modbus
    #
    def on_message(self, client, userdata, message):
        # Pour voir le message de debug contenant le topic entier, décommenter la ligne suivante
        #print(self.msg.topic+" "+str(self.msg.payload))
        # Traitement du topic reçu
        metrique = message.payload.decode()
        # Debug affichant le payload du topic traité
        print(metrique)
        # Appel de la methode "Nouvel_Indice_Modbus" du controleur 
        # en lui passant en paramètre le métrique précédemment
        self.controleur.Nouvel_Indice_Modbus(metrique)

    ##
	#   Boucle MQTT
	#
	# 	\brief Boucle infinie.
	#
	#   - Boucle permettant de gérer automatiquement la reconnexion au broker MQTT
    #
    def boucle(self):
            self.mqttclient.loop_forever()


class RecuperationTarif:    
    ## Constructeur
	#  \brief Constructeur de la Classe
    def __init__(self):
        # Ouverture du fichier de configuration 
        configuration = open("./config_Mysql.json","r")
        # Lecture du fichier de configuration 
        self.data = json.load(configuration)
        # Fermeture du fichier de configuration
        configuration.close() 

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
        #
        self.tarifHC = self.cursor.execute("SELECT montant_tarif FROM tarif NATURAL JOIN ressource WHERE nom_ressource='ELEC_HC' ORDER BY debut_tarif DESC LIMIT 1;")
        # Recherche de la données dans le curseur
        for (montant_tarif) in self.cursor:
            self.tarifHC = montant_tarif[0]
        # Premier requête : Prix du kWh Heure pleine
        self.tarifHP = self.cursor.execute("SELECT montant_tarif FROM tarif NATURAL JOIN ressource WHERE nom_ressource='ELEC_HP' ORDER BY debut_tarif DESC LIMIT 1;")
        # Recherche de la données dans le curseur
        for (montant_tarif) in self.cursor:
            self.tarifHP = montant_tarif[0]
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


class GestionDonnee:
     ## Constructeur
	#  \brief Constructeur de la Classe
    def __init__(self):
        # Ouverture du fichier de configuration 
        configuration = open("./config_Influxdb.json","r")
        # Lecture du fichier de configuration 
        self.data = json.load(configuration)
        # Fermeture du fichier de configuration
        configuration.close()

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
    def associerMetriqueTarif(self, metrique, tarifHC, tarifHP):
        # Calcule du coût total depuis la mise en service du compteur
        metrique = int(metrique)
        coutTotalHP = tarifHP * metrique
        coutTotalHC = tarifHC * metrique
        # Association du métrique avec les prix du kWh en une donnée
        self._data1 = Point("Modbus_data_test2").field("Prix du kWh HC", tarifHC).field("Prix du kWh HP", tarifHP).field("Consomation WH", metrique).field("Cout total HP", coutTotalHP).field("Cout total HC", coutTotalHC)
    
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


class Controleur:
    ## Constructeur
	#  \brief Constructeur de la Classe
    def __init__(self):
        # Déclaration des objets
        self.gestionMQTT = GestionMQTT(self)
        self.recuperationTarif = RecuperationTarif()
        self.gestionDonnee = GestionDonnee()
        self.gestionMQTT.boucle()

    def Nouvel_Indice_Modbus(self, metrique):
        # Appel des methodes permettant la récupération des derniers tarifs
        self.recuperationTarif.connexionBaseTarif()
        self.recuperationTarif.recupererTarif()
        tarifHC = self.recuperationTarif.get_tarif_HC()
        tarifHP = self.recuperationTarif.get_tarif_HP()
        # Appel des methodes permettant le traitement, 
        # ainsi que l'insertion des données dans la base influxdb
        self.gestionDonnee.connexionBaseMetrique()
        self.gestionDonnee.associerMetriqueTarif(metrique, tarifHC, tarifHP)
        self.gestionDonnee.envoieDonnées()

if __name__ == "__main__":
    # Création de l'objet Controleur
    controleur = Controleur()
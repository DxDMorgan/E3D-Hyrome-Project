##
#   \file E3D_GestionModbus.py
#   \brief Fichier GestionModbus 
#
#   Traitement des données Modbus
#
#
#   \class GestionModbus
#   \brief Classe GestionModbus.
#
#   Permet de gérer la récupération des métrique d'un compteur Modbus
#   \author Awen Ruaud
#   \version 1.0
#   \date  19 Mai 2021
#
from pyModbusTCP.client import ModbusClient
import paho.mqtt.client as mqtt
import time
import json

class GestionModbus:

    ## Constructeur
	#  \brief Constructeur de la Classe
    def __init__(self, sortieEnergieTotale):
        # Ouverture du fichier de configuration
        configuration = open("./config_Modbus.json","r")
        # Lecture du fichier de configuration 
        self.data = json.load(configuration)
        # Fermeture du fichier de configuration
        configuration.close()
        self.sortieEnergieTotale = sortieEnergieTotale

    ##
	#   Connexion à l'esclave Modbus
	#
	# 	\brief Connexion Modbus.
	#
	#   - Initialise la connexion avec l'esclave Modbus
    #
    def connexionCompteur(self):
        # Récupération des informatons de connexion
        self.SERVER_HOST = self.data["SERVER_HOST"]
        self.SERVER_PORT = self.data["SERVER_PORT"]
        # Création d'un client Modbus 
        self.c = ModbusClient()

        # décommentez cette ligne pour voir le message de débogage
        #self.c.debug(True)
        # Défini les paramètres du serveur modbus (adresse hote et port)
        self.c.host(self.SERVER_HOST)
        self.c.port(self.SERVER_PORT)

        # Ouvrir ou reconnecter TCP au serveur
        if not self.c.is_open():
            if not self.c.open():
                print("unable to connect to "+self.SERVER_HOST+":"+str(self.SERVER_PORT))

    ##
	#   Traitement Modbus
	#
	# 	\brief Traitement Modbus.
	#
	#   - Traite les registre de données reçu par le compteur Modbus
    #
    def recupererEnergie(self):
        # Si open () est ok, lire le registre (fonction modbus 0x03)
        if self.c.is_open():
            # Lire 2 registres à l'adresse 2566, stocker le résultat dans la liste des regs
            energieTotal = self.c.read_input_registers(0X0A06, 4)
            # Si la lecture du regitre est un succès, on enregistre les valeurs reçu
            if energieTotal:
                wh = energieTotal[0]*65536+energieTotal[1]
                Mwh = energieTotal[2]*65536+energieTotal[3]
                self.sortieEnergieTotale = wh + (Mwh*1000000)

    ##
	#   Publication MQTT
	#
	# 	\brief Publication métrique.
	#
	#   - Plublication du métrique reçu sur le broker MQTT
    #
    def publicationMetrique(self):
        # Création d'un client MQTT
        self.client = mqtt.Client()
        # Connexion au broker MQTT
        self.client.connect("51.254.200.114", 1883, 60)
        # Publication de l'indice "sortieEnergie"
        self.client.publish("Enerium/Modbus1/indice", payload=self.sortieEnergieTotale, qos=0, retain=True)

    ## Récuperer énergie totale
	#  \brief Récupère l'energie totale du compteur Modbus
    def get_energieTotale(self):
        return self.sortieEnergieTotale



if __name__ == "__main__":
    metrique = 0
    while True:
        # Creation de l'object GestionModbus
        a = GestionModbus(0)
        # Appel des méthodes
        a.connexionCompteur()
        a.recupererEnergie()
        metrique = a.get_energieTotale()
        # Ecrire la valeur obtenue
        print(metrique)
        a.publicationMetrique()
        # En sommeil pendant 30 minutes avant le prochain polling
        time.sleep(1800)
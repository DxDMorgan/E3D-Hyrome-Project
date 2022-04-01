##
#   \file Controller.py
#   \brief Fichier Controller
#
#   Controller synchronisant toutes les classes
#
#
#   \class RecuperationTarif
#   \brief Classe RecuperationTarif.
#
#   Permet de l'utilisation de toutes les classes
#   \author Awen Ruaud
#   \version 1
#   \date  31 Mai 2021
#

# Importation des classe du projet E3D
from E3D_GestionModbus import GestionModbus
from E3D_RecuperationTarif import RecuperationTarif
from E3D_GestionDonnee import GestionDonnee
# Importation des librairie time, et mysql.connector
import time
import mysql.connector
from mysql.connector import errorcode

if __name__ == "__main__":
    # Initialisation des variables
    metrique = 0
    tarif_hc = 0
    tarif_hp = 0
    while True:
        # Creation de l'object GestionModbus
        a = GestionModbus(0)
        # Appel des méthodes
        a.connexionCompteur()
        a.recupererEnergie()
        metrique = a.get_energieTotale()

        # Création de l'objet RecuperationTarif
        b = RecuperationTarif(0, 0)
        try:
            # Essaie de la connexion
            b.connexionBaseTarif()
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
            b.recupererTarif()
            tarif_hc = b.get_tarif_HC()
            tarif_hp = b.get_tarif_HP()
        
        # Création de l'objet GestionDonnee
        c = GestionDonnee(tarif_hc[0], tarif_hp[0], metrique)
        # Appel des méthodes
        c.connexionBaseMetrique()
        c.associerMetriqueTarif()
        c.envoieDonnées()
        # En sommeil pendant 30 minutes avant le prochain polling
        time.sleep(1800)
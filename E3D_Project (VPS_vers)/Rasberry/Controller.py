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

# Importation de la classe GestionModbus du projet E3D
from E3D_GestionModbus import GestionModbus
# Importation des librairie time
import time

if __name__ == "__main__":
    # Initialisation des variables
    metrique = 0
    while True:
        # Creation de l'object GestionModbus
        a = GestionModbus(0)
        # Appel des méthodes
        a.connexionCompteur()
        a.recupererEnergie()
        metrique = a.get_energieTotale()
        a.publicationMetrique()
        # En sommeil pendant 30 minutes avant le prochain polling
        time.sleep(1800)

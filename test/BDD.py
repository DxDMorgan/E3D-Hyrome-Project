import json
import mysql.connector

class BDD:
    def __init__(self):
        fic = open("config.json","r")
        self.data = json.load(fic)
        fic.close()

    def connecter(self):
        
        self.conn = mysql.connector.connect(host=self.data["serveur"],
                                         database=self.data["bdd"],
                                         user=self.data["utilisateur"],
                                         password=self.data["mdp"])
        self.conn.autocommit = True


    def fermer(self):
        self.conn.close()

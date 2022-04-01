import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'morgan',
  'password': 'msql49',
  'host': '127.0.0.1',
  'database': 'e3d',
  'raise_on_warnings': True
}

try:
  cnx = mysql.connector.connect(**config)
  cursor = cnx.cursor()
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
    query_eau = ("SELECT `montant_tarif` FROM `tarif` WHERE `id_ressource`= 1 AND CURRENT_DATE BETWEEN `debut_tarif` AND `fin_tarif`")
    cursor.execute(query_eau)
    for(montant_tarif) in cursor:
        print("Le tarif actuel de l'eau est de {}€".format(montant_tarif))
    
    query_elecHC = ("SELECT `montant_tarif` FROM `tarif` WHERE `id_ressource`= 2 AND CURRENT_DATE BETWEEN `debut_tarif` AND `fin_tarif`")
    cursor.execute(query_elecHC)
    for(montant_tarif) in cursor:
        print("Le tarif actuel de l'électricité (HC) est de {}€".format(montant_tarif))

    query_elecHP = ("SELECT `montant_tarif` FROM `tarif` WHERE `id_ressource`= 3 AND CURRENT_DATE BETWEEN `debut_tarif` AND `fin_tarif`")
    cursor.execute(query_elecHP)
    for(montant_tarif) in cursor:
        print("Le tarif actuel de l'électricité (HP) est de {}€".format(montant_tarif))
    
    query_gaz = ("SELECT `montant_tarif` FROM `tarif` WHERE `id_ressource`= 4 AND CURRENT_DATE BETWEEN `debut_tarif` AND `fin_tarif`")
    cursor.execute(query_gaz)
    for(montant_tarif) in cursor:
        print("Le tarif actuel du gaz est de {}€".format(montant_tarif))
    cnx.close()
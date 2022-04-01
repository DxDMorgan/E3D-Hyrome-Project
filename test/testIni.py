from configparser import ConfigParser
maConfigue = ConfigParser()

maConfigue.read('config.cfg')
print(maConfigue["Serveur"]["hote"])

session = maConfigue["Session"]
print(session["duree"])

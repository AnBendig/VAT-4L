from configparser import ConfigParser
from os.path import exists


class Configuration:
    """
    Klasse zur Verwaltung der in der Konfigurationsdatei gepflegten Informationen.
    Verwendet das Modul ConfigParser für den Informationsaustausch.

    Autor:      Andreas Bendig
    Erstellt:   30.03.2023
    Version:    0.1
    """
    def __init__(self):
        # Initialisieren der Attribute der Klasse

        self.system = None          # Ziel-Betriebssystem
        self.root_folder = None     # Root(Wurzel)- Ordner
        self.log_file_path = None   # Pfad zur Log-Datei
        self.db_server = None       # Name des Zielservers
        self.db_name = None         # Name der Datenbank
        self.db_user = None         # Benutzername der Datenbank
        self.db_password = None     # Passwort des verwendeten Benutzers TODO: Verschlüsselt ablegen

        self.isConfigurationNeeded = True    # Konfiguration muss eingestellt werden

    def load(self):
        config = ConfigParser()
        if exists('config.ini'):
            config = ConfigParser()
            config.read('config.ini')

            self.system = config["ROOT"]["system"]
            self.root_folder = config["ROOT"]["path"]

            if config.has_option("ROOT","log_file_path"):
                self.log_file_path = config["ROOT"]["log_file_path"]

            self.db_name = config["DATABASE"]["db_name"]
            self.db_user = config["DATABASE"]["db_user"]
            self.db_password = config["DATABASE"]["db_password"]
            self.db_server = config["DATABASE"]["db_server"]

            self.isConfigurationNeeded = False
        else:
            self.createConfigFile()

    @staticmethod
    def createConfigFile():
        config = ConfigParser()
        config["ROOT"] = {
            "system": "",
            "path": "",
            "log_file_path": ""
        }
        config["DATABASE"] = {
            "db_name": "",
            "db_user": "",
            "db_password": "",
            "db_server": ""
        }
        with open("config.ini", "w") as f:
            config.write(f)

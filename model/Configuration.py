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

        self.str_system = None          # Ziel-Betriebssystem
        self.str_root_folder = None     # Root(Wurzel)- Ordner
        self.strs_ignore_extensions: str = []    # Datei-Endungen, welche ignoriert werden sollen
        self.str_log_file_path = None   # Pfad zur Log-Datei
        self.str_db_server = None       # Name des Zielservers
        self.str_db_name = None         # Name der Datenbank
        self.str_db_user = None         # Benutzername der Datenbank
        self.str_db_password = None     # Passwort des verwendeten Benutzers TODO: Verschlüsselt ablegen
        self.str_db_port = ""           # Port für den Zugriff auf die Datenbank

        self.bol_is_configuration_needed = True    # Konfiguration muss eingestellt werden

    def load(self):
        config = ConfigParser()
        if exists('config.ini'):
            config = ConfigParser()
            config.read('config.ini')

            self.str_system = config["ROOT"]["system"]
            self.str_root_folder = config["ROOT"]["path"]
            self.strs_ignore_extensions = config["ROOT"]["ignore_extension"].split(";")

            if config.has_option("ROOT","log_file_path"):
                self.str_log_file_path = config["ROOT"]["log_file_path"]

            self.str_db_name = config["DATABASE"]["db_name"]
            self.str_db_user = config["DATABASE"]["db_user"]
            self.str_db_password = config["DATABASE"]["db_password"]
            self.str_db_server = config["DATABASE"]["db_server"]
            self.str_db_port = config["DATABASE"]["db_port"]

            self.bol_is_configuration_needed = False
        else:
            self.createConfigFile()

    @staticmethod
    def createConfigFile():
        config = ConfigParser()
        config["ROOT"] = {
            "system": "",
            "path": "",
            "log_file_path": "",
            "ignore_extension": ".sock;.lnk"
        }
        config["DATABASE"] = {
            "db_name": "",
            "db_user": "",
            "db_password": "",
            "db_server": "",
            "db_port": "3306"
        }
        with open("config.ini", "w") as f:
            config.write(f)

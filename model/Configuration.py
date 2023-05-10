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
    def __init__(self, appPath : str):
        """
        Initialisiert ein Objekt dieser Klasse.
        """

        self.str_system = None          # Ziel-Betriebssystem
        self.str_root_folder = None     # Root(Wurzel)- Ordner
        self.strs_ignore_extensions: list = []    # Datei-Endungen, welche ignoriert werden sollen
        self.str_log_file_path = None   # Pfad zur Log-Datei
        self.str_db_server = None       # Name des Zielservers
        self.str_db_name = None         # Name der Datenbank
        self.str_db_user = None         # Benutzername der Datenbank
        self.str_db_password = None     # Passwort des verwendeten Benutzers TODO: Verschlüsselt ablegen
        self.str_db_port = ""           # Port für den Zugriff auf die Datenbank
        self.str_appPath = appPath      # Anwendungspfad
        self.str_configPath= self.str_appPath + '/config.ini' # Pfad zur Konfigurationsdatei

        self.bol_is_configuration_needed = True    # Konfiguration muss eingestellt werden

    def load(self):
        """
        Liest die Datei 'config.ini' aus dem Anwendungsverzeichnis und lädt die beinhalteten Parameter.

        :return:
        Keine Rückgabe
        """

        # Überprüfung, ob Konfigurationsdatei im Anwendungsverzeichnis vorhanden ist
        if exists(self.str_configPath):
            # Konfigurationsdatei vorhanden
            config = ConfigParser()
            config.read(self.str_configPath)

            # Lesen der ROOT-Parameter
            self.str_system = config["ROOT"]["system"]
            self.str_root_folder = config["ROOT"]["path"]
            self.strs_ignore_extensions = config["ROOT"]["ignore_extension"].split(";")

            if config.has_option("ROOT","log_file_path"):
                self.str_log_file_path = config["ROOT"]["log_file_path"]

            # Lesen der DATABASE-Parameter
            self.str_db_name = config["DATABASE"]["db_name"]
            self.str_db_user = config["DATABASE"]["db_user"]
            self.str_db_password = config["DATABASE"]["db_password"]
            self.str_db_server = config["DATABASE"]["db_server"]
            self.str_db_port = config["DATABASE"]["db_port"]

            self.bol_is_configuration_needed = False    # Konfiguration erfolgreich gelesen - keine Konfiguration notwendig.
        else:
            # Konfigurationsdatei nicht vorhanden, erstelle eine neue, leere Datei im Anwendungsverzeichnis.
            self.createConfigFile(self.str_configPath)

    @staticmethod
    def createConfigFile(str_configPath : str):
        """
        Methode erstellt eine neue, mit Basiswerten gefüllte Konfigurationsdatei.
        :return:
        Keine Rückgabe
        """
        config = ConfigParser()

        # Erstellung der Parameter für ROOT-Einträge:
        config["ROOT"] = {
            "system": "",
            "path": "",
            "log_file_path": "",
            "ignore_extension": ".sock;.lnk"
        }

        #Erstellung der Parameter für DATABASE-Einträge
        config["DATABASE"] = {
            "db_name": "",
            "db_user": "",
            "db_password": "",
            "db_server": "",
            "db_port": "3306"
        }

        # Schreiben der Daten in die Datei
        with open(str_configPath, "w") as f:
            config.write(f)

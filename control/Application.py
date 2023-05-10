from control.SQLConnect import SQLConnect
import os
from datetime import datetime
from model.Configuration import Configuration


class Application:

    def __init__(self, str_app_path : str):
        self.AppPath : str = str_app_path
        self.Config : Configuration = self._get_config()
        self.Connection : SQLConnect = self._get_sql_connection()

    def _get_sql_connection(self) -> SQLConnect:
        # Verbindung zur Datenbank herstellen
        sql_connector: SQLConnect = SQLConnect()
        try:
            sql_connector.createConnection(self.Config.str_db_server,
                                           self.Config.str_db_port,
                                           self.Config.str_db_user,
                                           self.Config.str_db_password,
                                           self.Config.str_db_name)
            sql_connector.set_cursor(False)
        except Exception as ex:
            print(str(datetime.now()) + "Es konnte keine Verbindung zur Datenbank hergestellt werden. Der Vorgang wird abgebrochen. " + getattr(ex, 'msg'))
            exit(1011)
        finally:
            return sql_connector
    def _get_config(self) -> Configuration:
        # Auslesen der Konfigurationsdatei
        config: Configuration = Configuration(self.AppPath)
        config.load()

        # Prüfen, ob Konfiguration geladen werden konnte/gefüllt ist
        if config.bol_is_configuration_needed:
            print(
                str(datetime.now()) + "Bitte öffnen Sie die Konfiguration, tragen die notwendigen Daten ein und speichern diese.")
            exit(1010)
        else:
            return config


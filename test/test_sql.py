from model.Configuration import Configuration
from model.SQLConnect import SQLConnect
from control.JobCompare import JobCompare
from json import JSONEncoder

import json

Config = Configuration()
Config.load()

# Prüfen, ob Konfiguration geladen werden konnte/gefüllt ist
if Config.bol_is_configuration_needed:
    print("Bitte öffnen Sie die Konfiguration, tragen die notwendigen Daten ein und speichern diese.")
    exit(1010)

#Verbiundung zur Datenbank herstellen
sql_connector: SQLConnect = SQLConnect()
try:
    sql_connector.createConnection(Config.str_db_server,
                               Config.str_db_port,
                               Config.str_db_user,
                               Config.str_db_password,
                               Config.str_db_name)
except Exception as ex:
    print("Es konnte keine Verbindung zur Datenbank hergestellt werden. Der Vorgang wird abgebrochen. " + getattr(ex,'msg'))
    exit(1011)

sql_connector.set_cursor(True)

str_query = "SELECT * FROM tbl_scan WHERE job_id=1"
result_source = sql_connector.readData(str_query)

str_query = "SELECT * FROM tbl_scan WHERE job_id=3"
result_dest = sql_connector.readData(str_query)

my_compare= JobCompare(result_source, result_dest)


from fastapi import FastAPI
from json import dumps
from model.Configuration import Configuration
from model.SQLConnect import SQLConnect

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

sql_connector.set_cursor(False)

application = FastAPI()


"""
jobs = [
    {"job_id" : "1", "dt_job_start" : "2023-03-14 12:45:58", "dt_joc_end": "2023-03-14 12:45:59"},
    {"job_id" : "2", "dt_job_start" : "2023-03-16 13:20:14", "dt_joc_end": "2023-03-16 13:20:15"},
    {"job_id" : "3", "dt_job_start" : "2023-03-19 12:23:15", "dt_joc_end": "2023-03-19 12:23:16"},
    {"job_id" : "4", "dt_job_start" : "2023-03-25 14:45:02", "dt_joc_end": "2023-03-25 14:45:04"},
]
"""

@application.get("/jobs")
async def get_job_list():
    str_query = "SELECT * FROM `tbl_job`"
    result= sql_connector.readData(str_query)
    js = dumps(result, default=str)

    return js


@application.get("/jobs/{job_id}")
async def get_job_by_id(job_id : int):
    str_query = "SELECT * FROM `tbl_job`"
    result = sql_connector.readData(str_query)

    if (job_id.__le__(len(result)) and job_id.__gt__(0)):
        return dumps(result[job_id - 1], default=str)
    else:
        return "Index out of bounds!"

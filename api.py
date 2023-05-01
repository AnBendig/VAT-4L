import json

from fastapi import FastAPI
from json import dumps
from model.Configuration import Configuration
from model.SQLConnect import SQLConnect
from fastapi.middleware.cors import CORSMiddleware





# Konfiguration laden
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

application = FastAPI()

origins = ["*"]

application.add_middleware(CORSMiddleware,
                           allow_origins=origins,
                           allow_credentials=True,
                           allow_methods=["*"],
                           allow_headers=["*"],
                           )

@application.get("/vat4l-api")
async def get_api_info():
    return "VAT-4L API is working"

@application.get("/vat4l-api/jobs")
async def get_job_list():
    str_query = "SELECT * FROM tbl_job"
    result= sql_connector.readData(str_query)
    # return dumps(result, default=str)
    return result

@application.get("/vat4l-api/jobs/{job_id}")
async def get_job_by_id(job_id : int):
    str_query = "SELECT * FROM `tbl_job`"
    result = sql_connector.readData(str_query)

    if job_id.__le__(len(result)) and job_id.__gt__(0):
        # return dumps(result[job_id - 1], default=str)
        return result
    else:
        return "Index out of bounds!"

@application.get("/vat4l-api/dirs{job_id}")
async def get_directories(job_id: int):
    str_query = "SELECT * FROM `tbl_scan` WHERE is_directory=TRUE AND job_id=" + str(job_id) + " ORDER BY path ASC"
    result = sql_connector.readData(str_query)

    # return dumps(result, default=str)
    return result
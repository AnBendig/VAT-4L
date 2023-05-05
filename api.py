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
    result = sql_connector.readData(str_query)
    return result

@application.get("/vat4l-api/getjob/{job_id}")
async def get_job_by_id(job_id : int):

    str_query = "SELECT * FROM tbl_job WHERE id_job=" + str(job_id)

    result = sql_connector.readData(str_query)
    return result


@application.get("/vat4l-api/dirs/{job_id}")
async def get_directories(job_id: int):
    str_query = "SELECT * FROM `tbl_scan` WHERE is_directory=TRUE AND job_id=" + str(job_id) + " ORDER BY path"
    result = sql_connector.readData(str_query)

    return result

@application.get("/vat4l-api/comparejobs/{source_id}/{target_id}")
async def get_compare_jobs(source_id : int, target_id : int):
    # str_query = "SELECT s.id as source_id, t.id as target_id, s.path as path, s.job_id as source_job_id, t.job_id as target_job_id, s.size as source_size, t.size as target_size, s.hash as source_hash, t.hash as target_hash, s.user_name as source_user_name, t.user_name as target_user_name, s.group_name as source_group_name, t.group_name as target_group_name, s.filemode as source_filemode, t.filemode as target_filemode, s.created_date as source_created_date, t.created_date as target_created_date, s.modified_date as source_modified_date, t.modified_date as target_modified_date FROM tbl_scan AS s JOIN tbl_scan AS t ON s.path=t.path WHERE s.job_id="+str(source_id)+" AND t.job_id="+str(target_id)+" AND (s.hash!=t.hash OR s.user_id!=t.user_id OR s.group_id!=t.group_id OR s.filemode!=t.filemode)"
    str_query= "SELECT t.* FROM tbl_scan AS s JOIN tbl_scan AS t ON s.path=t.path WHERE s.job_id="+str(source_id)+" AND t.job_id="+str(target_id)+" AND (s.hash!=t.hash OR s.user_id!=t.user_id OR s.group_id!=t.group_id OR s.filemode!=t.filemode)"
    result = sql_connector.readData(str_query)

    return result

@application.get("/vat4l-api/getdelta/{source_id}/{target_id}")
async def get_delta_jobs(source_id: int, target_id : int):
    str_query = "SELECT * FROM ( SELECT * FROM tbl_scan s WHERE s.job_id="+ str(source_id) +" UNION ALL SELECT * FROM tbl_scan t WHERE t.job_id="+ str(target_id) +") tbl_scan GROUP BY path HAVING COUNT(*) = 1"
    result = sql_connector.readData(str_query)

    return result

@application.get("/vat4l-api/getpathlist")
async def get_path_list() :
    str_query : str = "SELECT DISTINCT path, id FROM tbl_scan WHERE is_directory=TRUE GROUP BY path"
    result = sql_connector.readData(str_query)

    return result


@application.get("/vat4l-api/getfilebypath/{selectedPathID}")
async def get_path_list(selectedPathID) :
    str_query : str = "SELECT * FROM tbl_scan WHERE is_directory=FALSE AND job_id=8 AND path=CONCAT((SELECT d.path FROM tbl_scan as d WHERE d.id=" + selectedPathID + "),'/',file_name) GROUP BY hash"
    result = sql_connector.readData(str_query)

    return result

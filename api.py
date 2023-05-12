import os

from fastapi import FastAPI
from model.Configuration import Configuration
from control.SQLConnect import SQLConnect
from fastapi.middleware.cors import CORSMiddleware

appPath : str = os.path.dirname(__file__)

# Konfiguration laden
Config = Configuration(appPath)
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
    """Abfrage zum Test der Verfügbarkeit der API."""
    return "VAT-4L API is working"

@application.get("/vat4l-api/jobs")
async def get_job_list():
    """Liefert eine Liste aller Jobs aus der Tabelle tbl_job"""
    str_query = "SELECT * FROM tbl_job"
    result = sql_connector.readData(str_query)
    return result

@application.get("/vat4l-api/getjob/{job_id}")
async def get_job_by_id(job_id : int):
    """
    Liefert Daten zu einem ausgwählten Job.
    :param job_id ID des zu ladenden Jobs."""
    str_query = "SELECT * FROM tbl_job WHERE id_job=" + str(job_id)

    result = sql_connector.readData(str_query)
    return result


@application.get("/vat4l-api/dirs/{job_id}")
async def get_directories(job_id: int):
    """
    Liefert eine Liste aller Verzeichnisse zurück, welche unterhalb des Root-Ordners während eines Jobs gefunden wurden.
    :param job_id: Integer. Der Job, für welchen die Verzeichnisse zurückgegeben werden soll
    :return: Dictionary. Alle Verzeichnisse des ausgewählten Jobs.
    """
    str_query = "SELECT * FROM `tbl_scan` WHERE is_directory=TRUE AND job_id=" + str(job_id) + " ORDER BY path"
    result = sql_connector.readData(str_query)

    return result

@application.get("/vat4l-api/comparejobs/{source_id}/{target_id}")
async def get_compare_jobs(source_id : int, target_id : int):
    """
    Vergleicht zwei Jobs miteinander und liefert eine Liste der Unterschiede zurück.
    Verglichen werden die Dateiattribute Filemode, User- und Group-ID sowie der Hash-Wert der Datei.

    :param source_id: Integer. Job-ID des ersten Jobs.
    :param target_id: Integer. Job-ID des zweiten Jobs.
    :return: Dictionary. Liefert eine Liste aller unterschiedlichen Dateien zurück.
    """

    # str_query= "SELECT t.* FROM tbl_scan AS s JOIN tbl_scan AS t ON s.path=t.path WHERE s.job_id="+str(source_id)+" AND t.job_id="+str(target_id)+" AND (s.hash!=t.hash OR s.user_id!=t.user_id OR s.group_id!=t.group_id OR s.filemode!=t.filemode)"
    str_query = "SELECT t.path as path,	t.size as size, s.size as s_size, t.group_name as group_name, s.group_name as s_group_name, t.user_name as user_name, s.user_name as s_user_name, t.filemode as filemode, s.filemode as s_filemode, t.created_date as created_date, s.created_date as s_created_date, t.modified_date as modified_date, s.modified_date as s_modified_date" \
                " FROM tbl_scan AS s JOIN tbl_scan AS t ON s.path=t.path WHERE s.job_id=" + str(
        source_id) + " AND t.job_id=" + str(
        target_id) + " AND (s.hash!=t.hash OR s.user_id!=t.user_id OR s.group_id!=t.group_id OR s.filemode!=t.filemode)"
    result = sql_connector.readData(str_query)

    return result

@application.get("/vat4l-api/getdelta/{source_id}/{target_id}")
async def get_delta_jobs(source_id: int, target_id : int):
    """
    Ermittelt die Unterschiede zwischen zwei Jobs. Liefert eine Liste aus Einträgen, welche im Ziel-Job hinzugefügt oder gelöscht worden sind.

    :param source_id: Integer. Job-ID des ersten Jobs
    :param target_id: Integer. Job-ID des zweiten Jobs
    :return: Dictionary. Eine Liste der Dateien, welche hinzugefügt oder gelöscht worden sind.
    """
    str_query = "SELECT * FROM ( SELECT * FROM tbl_scan s WHERE s.job_id="+ str(source_id) +" UNION ALL SELECT * FROM tbl_scan t WHERE t.job_id="+ str(target_id) +") tbl_scan GROUP BY path HAVING COUNT(*) = 1"
    result = sql_connector.readData(str_query)

    return result

@application.get("/vat4l-api/getpathlist")
async def get_path_list() :
    """
    Liefert eine Liste aller Verzeichnisse zurück
    :return: Dictionary. Liste aller Verzeichnise
    """
    str_query : str = "SELECT DISTINCT path, id FROM tbl_scan WHERE is_directory=TRUE GROUP BY path"
    result = sql_connector.readData(str_query)

    return result


@application.get("/vat4l-api/getfilebypath/{selectedPathID}")
async def get_path_list(selectedPathID) :
    """
    Liefert eine Übersicht für alle Änderungen in einem Verzeichnis zurück.

    :param selectedPathID: Integer. Die ID des Dateipfads.
    :return: Dictionary. Liste aller Dateien in dem Verzeichnis.
    """
    str_query : str = "SELECT * FROM tbl_scan WHERE is_directory=FALSE AND job_id=8 AND path=CONCAT((SELECT d.path FROM tbl_scan as d WHERE d.id=" + selectedPathID + "),'/',file_name) GROUP BY hash"
    result = sql_connector.readData(str_query)

    return result

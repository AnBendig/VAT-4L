import os.path
from datetime import datetime
from model.Configuration import Configuration
from control.SQLConnect import SQLConnect
from model.Job import Job
from control.JobHandler import JobHandler
from control.Application import Application

app : Application = Application(os.path.dirname(__file__))

"""
appPath : str = os.path.dirname(__file__)

# Auslesen der Konfigurationsdatei
Config : Configuration= Configuration(appPath)
Config.load()

# Prüfen, ob Konfiguration geladen werden konnte/gefüllt ist
if Config.bol_is_configuration_needed:
    print(str(datetime.now()) + "Bitte öffnen Sie die Konfiguration, tragen die notwendigen Daten ein und speichern diese.")
    exit(1010)

#Verbindung zur Datenbank herstellen
sql_connector: SQLConnect = SQLConnect()
try:
    sql_connector.createConnection(Config.str_db_server,
                               Config.str_db_port,
                               Config.str_db_user,
                               Config.str_db_password,
                               Config.str_db_name)
    sql_connector.set_cursor(False)
except Exception as ex:
    print(str(datetime.now()) + "Es konnte keine Verbindung zur Datenbank hergestellt werden. Der Vorgang wird abgebrochen. " + getattr(ex,'msg'))
    exit(1011)
"""

# Erstellung eines neuen Jobs für den Scan

JobHandler : JobHandler = JobHandler(app)

current_job: Job = Job()
int_last_job_id : int = JobHandler.get_last_jobid()

#current_job.create_job(sql_connector)
current_job.create_job(app.Connection)

# Scan der Verzeichnisse durchführen
JobHandler.execute_job(current_job)

# current_job.endJob(sql_connector)
current_job.endJob(app.Connection)

# Überprüfung durchführen, ob der aktuelle Job mit dem vorherigem inhaltlich identisch ist
if JobHandler.is_equal_to_previous(int_last_job_id, current_job.job_id):
    # Job ist identisch und kann gelöscht werden
    print(str(datetime.now()) + ": Job " + str(current_job.job_id) + " ist identisch mit vorherigem Lauf (Job " + str(int_last_job_id) + "). Daten werden gelöscht.")
    JobHandler.delete_job(current_job.job_id)
else:
    # Ausgabe der Verarbeitung
    print(str(datetime.now()) + ": Scan abgeschlossen. Anzahl der gescannten Verzeichnisse/Dateien: " + str(current_job.int_processed_dir) + "/" + str(current_job.int_processed_file) +" - Dauer: " + str(current_job.int_job_duration) + " mics")



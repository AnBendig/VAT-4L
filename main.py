import os.path
from datetime import datetime

from model.Configuration import Configuration
from model.DirectoryScanner import DirectoryScanner
from model.SQLConnect import SQLConnect
from model.Job import Job

appPath : str = os.path.dirname(__file__)

# Auslesen der Konfigurationsdatei
Config : Configuration= Configuration(appPath)
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
    sql_connector.set_cursor(False)
except Exception as ex:
    print(str(datetime.now()) + "Es konnte keine Verbindung zur Datenbank hergestellt werden. Der Vorgang wird abgebrochen. " + getattr(ex,'msg'))
    exit(1011)

# Erstellung eines neuen Jobs für den Scan

current_job: Job = Job()
int_last_job_id : int = current_job.get_last_jobid(sql_connector)

current_job.create_job(sql_connector)

# Objekt vom Verzeichnis-Scanner erzeugen
dirScanner = DirectoryScanner(Config, sql_connector, current_job)

# Scan starten
dirScanner.startScan()

# Verarbeitungsparameter im Job speichern
current_job.endJob(sql_connector)

# Überprüfung durchführen, ob der aktuelle Job mit dem vorherigem inhaltlich identisch ist
if (current_job.is_equal_to_previous(sql_connector,int_last_job_id)) :
    # Job ist identisch und kann gelöscht werden
    print("Job " + str(current_job.job_id) + " ist identisch mit vorherigem Lauf (Job " + str(int_last_job_id) + "). Daten werden gelöscht.")
    current_job.delete_job(sql_connector)
else:
    # Ausgabe der Verarbeitung
    print(str(datetime.now()) + ": Scan abgeschlossen. Anzahl der gescannten Verzeichnisse/Dateien: " + str(current_job.int_processed_dir) + "/" + str(current_job.int_processed_file) +" - Dauer: " + str(current_job.int_job_duration) + " mics")



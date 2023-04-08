from model.Configuration import Configuration
from model.DirectoryScanner import DirectoryScanner
from model.SQLConnect import SQLConnect
from model.Job import Job

# Auslesen der Konfigurationsdatei
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
    sql_connector.set_cursor(False)
except Exception as ex:
    print("Es konnte keine Verbindung zur Datenbank hergestellt werden. Der Vorgang wird abgebrochen. " + getattr(ex,'msg'))
    exit(1011)

# Erstellung eines neuen Jobs für den Scan
current_job: Job = Job()
current_job.create_job(sql_connector)

# Objekt vom Verzeichnis-Scanner erzeugen
dirScanner = DirectoryScanner(Config, sql_connector, current_job)

# Scan starten
dirScanner.startScan()

# Verarbeitungsparameter im Job speichern
current_job.endJob(sql_connector)

# Ausgabe der Verarbeitung
print("Anzahl der gescannten Verzeichnisse: " + str(current_job.int_processed_dir))
print("Anzahl der gescannten Dateien: " + str(current_job.int_processed_file))
print("Dauer der Ausführung: " + str(current_job.int_job_duration) + " mics")


from datetime import datetime, timedelta
from control import SQLConnect

class Job:
    """
    Klasse zur Verwaltung eines einzelnen Scan-Durchlaufes
    """
    def __init__(self):
        """
        Erstellt ein Objekt dieser Klasse.
        """
        self.job_id: int = 0                # Eindeutige ID des Vorgangs
        self.dt_job_start: datetime = None  # Startzeitpunkt des Vorgangs
        self.dt_job_end: datetime = None    # Endzeitpunkt des Vorgangs
        self.int_job_duration = 0           # Dauer der Ausführung
        self.int_processed_dir: int = 0     # Anzahl der verarbeiteten Verzeichnisse
        self.int_processed_file: int= 0     # Anzahl der verarbeiteten Dateien


    def createJob(self):
        """
        Erfasst der Startzeitpunkt des Scans
        :return:
        Keine Rückgabe
        """
        self.dt_job_start= datetime.now()

    def endJob(self, sql_connection: SQLConnect):
        """
        Legt der Endzeitpunkt des Scans fest und speichert die ermittelten Informationen zum Vorgang in der Datenbank.
        :param sql_connection:
            SQLConnect.
        :return:
        """
        self.dt_job_end = datetime.now()
        self.int_job_duration= self._get_runtime()

        # TODO: Umschreiben auf SQLQueryComposer:
        str_query: str = "UPDATE `tbl_job` SET "
        str_query += "`dt_start_job`='"+ str(self.dt_job_start.strftime('%Y-%m-%d %H:%M:%S')) +"',"
        str_query += "`dt_end_job`='"+ str(self.dt_job_end.strftime('%Y-%m-%d %H:%M:%S')) +"',"
        str_query += "`int_processed_dir`='" + str(self.int_processed_dir) + "',"
        str_query += "`int_processed_file`='" + str(self.int_processed_file) + "' "
        str_query += "WHERE id_job= '" + str(self.job_id) + "'"

        sql_connection.writeData(str_query)     # Übertragen der Daten in die Datenbank
        sql_connection.commit()                 # Speichern der Daten

    def create_job(self, sql_connection: SQLConnect) -> bool:
        """
         Erfasst der Startzeitpunkt des Scans und schreibt diese Informationen in die Datenbank
        :param sql_connection:
            SQLConnect.
        :return:
            Boolean. Liefert 'True', falls der Vorgang erfolgreich erstellt worden ist.
        """

        # Versuche, den Vorgang zu instanziieren
        try:
            self.dt_job_start = datetime.now()
            # Schreiben des Startzeitpunktes in die Datenbank
            str_query: str = "INSERT INTO tbl_job (`dt_start_job`) VALUES ('" + self.dt_job_start.strftime('%Y-%m-%d %H:%M:%S') + "')"
            sql_connection.writeData(str_query)

            # Ermittlung der, von der Datenbank generierten, ID für den Vorgang
            self.job_id = sql_connection.get_last_row_id()
            sql_connection.commit()

        except:
            # Der Job konnte nicht erstellt werden
            print('Neuer Job konnte nicht erstellt werden.')
            exit(1013)
        return True

    def _get_runtime(self) -> int:
        """
        Methode zur Ermittlung der Ausführungszeit für den Vorgang.
        :return:
            Integer. Zeitdauer in Mikrosekunden (mics)
        """
        diff: timedelta = self.dt_job_end - self.dt_job_start
        return diff.microseconds






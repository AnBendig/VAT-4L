from datetime import datetime, timedelta
from model import SQLConnect
class Job():
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

    def get_last_jobid (self, sql_connection: SQLConnect) -> int:
        str_query : str= "SELECT MAX(id_job) FROM tbl_job"
        result= sql_connection.readData(str_query)
        t : tuple= result[0]
        return result[0][0]

    def is_equal_to_previous (self, sql_connection : SQLConnect, int_previous_job_id : int) -> bool:
        """
        Vergleicht zwei Jobs miteinander und prüft, ob es Unterschiede zum vorherigem Job gibt.

        :param sql_connection: SQLConnect. Verbindung zur Datenbank.
        :param int_previous_job_id: Integer. Die Job-ID des vorherigen Jobs.
        :return: Boolean. Liefert Wahr, wenn beide Jobs identisch sind.
        """
        # Starte Überprüfung auf Änderungen von Dateien zwischen den Jobs
        bol_is_equal :bool = False
        str_query = "SELECT t.* FROM tbl_scan AS s JOIN tbl_scan AS t ON s.path=t.path WHERE s.job_id=" + str(int_previous_job_id) + " AND t.job_id=" + str(self.job_id) + " AND (s.hash!=t.hash OR s.user_id!=t.user_id OR s.group_id!=t.group_id OR s.filemode!=t.filemode)"
        result = sql_connection.readData(str_query)

        if (len(result) == 0) :
            # Falls die Abfrage auf Äderungen kein Ergebniss liefert, wird geprüft,
            # ob Dateien hinzugefügt oder gelöscht worden sind.
            str_query = "SELECT * FROM ( SELECT * FROM tbl_scan s WHERE s.job_id=" + str(int_previous_job_id) + " UNION ALL SELECT * FROM tbl_scan t WHERE t.job_id=" + str(self.job_id) + ") tbl_scan GROUP BY path HAVING COUNT(*) = 1"
            result = sql_connection.readData(str_query)
            if (len(result) == 0) :
                # Es wurden keine Dateien hinzugefügt oder gelöscht → Jobs sind inhaltlich identisch
                bol_is_equal = True

        return bol_is_equal

    def delete_job(self, sql_connection : SQLConnect) :
        """
        Löscht einen Job aus der Datenbank.

        :param sql_connection: SQLConnect. Verbindung zur Datenbank.
        :return: void.
        """

        # Lösche alle Dateien und Verzeichnisse des aktuellen Jobs aus der Datenbank
        str_query :str= "DELETE FROM tbl_scan WHERE job_id=" + str(self.job_id)
        sql_connection.writeData(str_query)

        # Lösche den aktuellen Job aus der Datenbank
        str_query: str = "DELETE FROM tbl_job WHERE id_job=" + str(self.job_id)
        sql_connection.writeData(str_query)

        # Setze den Zähler für das AUTO_INCREMENT zurück, um kontinuierliche Jobnummern zu erzeugen
        str_query: str = "ALTER TABLE tbl_job AUTO_INCREMENT = " + str(self.job_id)
        sql_connection.writeData(str_query)

        # Schreiben der Daten
        sql_connection.commit()
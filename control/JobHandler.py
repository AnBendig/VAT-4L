from model.Job import Job
from control.DirectoryScanner import DirectoryScanner
from control.Application import Application
from datetime import datetime

class JobHandler:

    def __init__(self, application : Application):
        self._App : Application = application

        # Objekt vom Verzeichnis-Scanner erzeugen
        self._DirectoryScanner : DirectoryScanner = DirectoryScanner(self._App)

    def execute_job(self) :
       """
       Führt einen Job aus.
       :return: keine Rückgabe.
       """
       current_job: Job = Job()
       int_last_job_id: int = self.get_last_jobid()

       # current_job.create_job(sql_connector)
       current_job.create_job(self._App.Connection)

       # Scan der Verzeichnisse durchführen
       self._DirectoryScanner.start_scan(current_job)

       # current_job.endJob(sql_connector)
       current_job.endJob(self._App.Connection)

       # Überprüfung durchführen, ob der aktuelle Job mit dem vorherigem inhaltlich identisch ist
       if self.is_equal_to_previous(int_last_job_id, current_job.job_id):
           # Job ist identisch und kann gelöscht werden
           print(str(datetime.now()) + ": Job " + str(
               current_job.job_id) + " ist identisch mit vorherigem Lauf (Job " + str(
               int_last_job_id) + "). Daten werden gelöscht.")
           self.delete_job(current_job.job_id)
       else:
           # Ausgabe der Verarbeitung
           print(str(datetime.now()) + ": Scan abgeschlossen. Anzahl der gescannten Verzeichnisse/Dateien: " + str(
               current_job.int_processed_dir) + "/" + str(current_job.int_processed_file) + " - Dauer: " + str(
               current_job.int_job_duration) + " mics")

    def get_last_jobid(self) -> int:
        """
        Liefert die letzte in der Datenbank erfasste Job-ID.
        :param self:
        :return:
        """
        str_query: str = "SELECT MAX(id_job) FROM tbl_job"
        result = self._App.Connection.readData(str_query)

        return result[0][0]

    def is_equal_to_previous (self, int_previous_job_id : int, int_current_job_id : int) -> bool:
        """
        Vergleicht zwei Jobs miteinander und prüft, ob es Unterschiede zum vorherigem Job gibt.

        :param int_previous_job_id: Integer. Die Job-ID des vorherigen Jobs.
        :param int_current_job_id: Integer. Die Job-ID des aktuellen Jobs.
        :return: Boolean. Liefert Wahr, wenn beide Jobs identisch sind.
        """
        # Starte Überprüfung auf Änderungen von Dateien zwischen den Jobs
        bol_is_equal :bool = False
        str_query = "SELECT t.* FROM tbl_scan AS s JOIN tbl_scan AS t ON s.path=t.path WHERE s.job_id=" + str(int_previous_job_id) + " AND t.job_id=" + str(int_current_job_id) + " AND (s.hash!=t.hash OR s.user_id!=t.user_id OR s.group_id!=t.group_id OR s.filemode!=t.filemode)"
        result = self._App.Connection.readData(str_query)

        if len(result) == 0:
            # Falls die Abfrage auf Änderungen kein Ergebnis liefert, wird geprüft,
            # ob Dateien hinzugefügt oder gelöscht worden sind.
            str_query = "SELECT * FROM ( SELECT * FROM tbl_scan s WHERE s.job_id=" + str(int_previous_job_id) + " UNION ALL SELECT * FROM tbl_scan t WHERE t.job_id=" + str(int_current_job_id) + ") tbl_scan GROUP BY path HAVING COUNT(*) = 1"
            result = self._App.Connection.readData(str_query)
            if len(result) == 0:
                # Es wurden keine Dateien hinzugefügt oder gelöscht → Jobs sind inhaltlich identisch
                bol_is_equal = True

        return bol_is_equal

    def delete_job(self, job_id : int) :
        """
        Löscht einen Job aus der Datenbank.
        :return: void.
        """

        # Lösche alle Dateien und Verzeichnisse des aktuellen Jobs aus der Datenbank
        str_query :str= "DELETE FROM tbl_scan WHERE job_id=" + str(job_id)
        self._App.Connection.writeData(str_query)

        # Lösche den aktuellen Job aus der Datenbank
        str_query: str = "DELETE FROM tbl_job WHERE id_job=" + str(job_id)
        self._App.Connection.writeData(str_query)

        # Setze den Zähler für das AUTO_INCREMENT zurück, um kontinuierliche Jobnummern zu erzeugen
        str_query: str = "ALTER TABLE tbl_job AUTO_INCREMENT =" + str(job_id)
        self._App.Connection.writeData(str_query)

        # Schreiben der Daten
        self._App.Connection.commit()
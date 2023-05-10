import os
from model.DirectoryEntry import DirectoryEntry
from model.FileEntry import FileEntry
from control.SQLConnect import SQLQueryComposer,SQLQueryType
from model.Job import Job
from control.Application import Application

class DirectoryScanner:
    """
    Klasse zur Verarbeitung der Verzeichnisstruktur ausgehend vom definierten ROOT-Verzeichnis aus der Konfigurationsdatei.
    """

    def __init__(self, application : Application):
        """
        Erstellt ein Objekt der Klasse.

        :param application:
            Application. Globales Anwendungsobjekt
        """
       # self._Config: Configuration = config
        self._App = application
        # self._sql_connector: SQLConnect= sql_connector
        self._FolderList: list = []   # Liste der zu untersuchenden Verzeichnisse
        self._FolderList.append(self._App.Config.str_root_folder) # Fügt das Wurzelverzeichnis der Liste hinzu
        self._currentJob: Job = None

    def start_scan(self, job : Job):
        """
        Startet den Scan der Verzeichnisse und speicher die Ergebnisse in der Datenbank
        :param job:
            Job. Der aktuelle Vorgang zum Scan der Verzeichnisstruktur.
        :return:
            Keine Rückgabe.
        """
        self._currentJob = job

        # Initialisiere die Zähler für Verzeichnisse und Dateien
        int_file_counter: int = 0
        int_dir_counter:int =0

        if len(self._FolderList) > 0:
            # Liste enthält zu verarbeitenden Verzeichnisse → lade das erste Element aus der Liste
            str_current_folder = next(iter(self._FolderList), None)

            while str_current_folder is not None:
                # Überprüfung des aktuellen Verzeichnisses

                with os.scandir(str_current_folder) as entries:

                    for entry in entries:
                        # Wiederhole für jedes Element im Verzeichnis

                        if entry.is_dir() and not entry.is_symlink():
                            # Element ist ein Ordner, aber kein SymLink

                            # Erstelle Verzeichnis-Objekt und initialisiere dieses
                            my_dir: DirectoryEntry = DirectoryEntry(self._App.Config)
                            my_dir.readEntry(entry)

                            # Überprüfung, ob das aktuelle Verzeichnis schon in der Bearbeitungsliste vorhanden ist.
                            if not (my_dir.str_path in self._FolderList) :
                                # Falls nicht, füge den Pfad der Liste hinzu
                                self._FolderList.append(my_dir.str_path)

                                # Verzeichniszähler um 1 erhöhen
                                int_dir_counter +=1

                                # Abfrage für das aktuelle Verzeichnis erstellen
                                str_query = self._build_query(my_dir)

                                # Übertragung an die Datenbank
                                self._App.Connection.writeData(str_query)
                        else:
                            # Überprüfung, ob Element ein SymLink ist
                            if not entry.is_symlink():
                                # Element ist eine Datei - Erstelle FileEntry Objekt
                                my_file: FileEntry = FileEntry(self._App.Config) # TODO: Reduzierung auf Extensions
                                my_file.readEntry(entry)

                                # Dateizähler um 1 erhöhen
                                int_file_counter +=1

                                # Erstellen der SQL-Anweisung
                                str_query= self._build_query(my_file)

                                # Übertragung der Daten an die Datenbank
                                self._App.Connection.writeData(str_query)

                # Speichern der Daten in der Datenbank
                self._App.Connection.commit()

                # entferne den aktuell verarbeiteten Ordner auf der Verzeichnisliste
                self._FolderList.remove(str_current_folder)

                # lade das nächste Verzeichnis aus der Verarbeitungsliste
                str_current_folder = next(iter(self._FolderList), None)

        # Übertrage die ermittelten Zählerstände an den aktuellen Job
        self._currentJob.int_processed_dir= int_dir_counter
        self._currentJob.int_processed_file= int_file_counter

    def _build_query(self, current_entry) -> str:
        """
        Methode erstellt mithilfe der Klasse SQLQueryComposer die Abfrage für die Datenbank
        :param current_entry:
            Variant. Erwartet wir ein Objekt der Klassen FileEntry oder DirectoryEntry
        :return:
            String. Die erstellte SQL-Anweisung.
        """
        sql_composer: SQLQueryComposer = SQLQueryComposer()

        # Hinzufügen der für beide Klassen verfügbaren Inhalte
        sql_composer.add("job_id", self._currentJob.job_id)
        sql_composer.add("is_directory", current_entry.bol_is_directory)
        sql_composer.add("path", current_entry.str_path)
        sql_composer.add("user_id", current_entry.int_user_id)
        sql_composer.add("user_name", current_entry.str_user_name)
        sql_composer.add("group_id", current_entry.int_group_id)
        sql_composer.add("group_name", current_entry.str_group_name)
        sql_composer.add("filemode", current_entry.str_filemode)
        sql_composer.add("created_date", current_entry.flt_created_date)
        sql_composer.add("modified_date", current_entry.flt_modified_date)

        if type(current_entry) is FileEntry:
            # Hinzufügen der für die Klasse FileEntry spezifischen Inhalte
            sql_composer.add("file_name", current_entry.str_name)
            sql_composer.add("extension", current_entry.str_extension)
            sql_composer.add("hash", current_entry.str_hash_value_md5)
            sql_composer.add("size", current_entry.int_size)

        #Generierung der Anweisung
        str_query = sql_composer.get_query(SQLQueryType.INSERT, "tbl_scan")

        return str_query
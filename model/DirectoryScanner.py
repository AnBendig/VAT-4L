from datetime import datetime
import os
from model.DirectoryEntry import DirectoryEntry
from model.Entry import Entry
from model.Configuration import Configuration
from model.SQLConntect import SQLConnect


class DirectoryScanner:
    """

    """

    def __init__(self, config):
        #  Initialisierung der Attribute
        if config is None:
            pass

        self._Config: Configuration = config
        self._FolderList = []
        self._FolderList.append(self._Config.str_root_folder)

    def startScan(self):
        sql_connector: SQLConnect = SQLConnect()
        sql_connector.createConnection(self._Config.str_db_server,
                                       "3306",
                                       self._Config.str_db_user,
                                       self._Config.str_db_password,
                                       "vat4l")

        print("starte Scan...")

        flt_ts_start= datetime.timestamp(datetime.now())


        int_file_counter: int = 0
        int_dir_counter:int =0

        if len(self._FolderList) > 0:
            str_current_folder = next(iter(self._FolderList), None)

            while str_current_folder is not None:
                self._FolderList.remove(str_current_folder)
                with os.scandir(str_current_folder) as entries:
                    for entry in entries:
                        if entry.is_dir():
                            my_dir: DirectoryEntry = DirectoryEntry(self._Config)
                            my_dir.readEntry(entry)
                            if my_dir.bol_is_directory :
                                self._FolderList.append(my_dir.str_path)

                                int_dir_counter +=1
                                print("Verzeichnis: " + my_dir.str_path)
                                print(" --> Erstellt am: " + my_dir.flt_created_date.strftime ('%Y-%m-%d %H:%M:%S'))  # TODO: Nur für Windows-Systeme
                                print(" --> Letze Bearbeitung: " + my_dir.flt_modified_date.strftime ('%Y-%m-%d %H:%M:%S'))
                                print(" --> User ID: " + str(my_dir.int_group_id))
                                print(" --> Group ID: " + str(my_dir.int_group_id))

                        else:
                            my_file: Entry = Entry(self._Config)

                            if not entry.is_symlink():
                                my_file.readEntry(entry)

                                int_file_counter +=1
                                print("Datei: " + my_file.str_name)
                                print(" --> Dateigröße: " + str(my_file.int_size) + " Bytes")
                                print(" --> Erstellt am: " + my_file.flt_created_date.strftime ('%Y-%m-%d %H:%M:%S'))  # TODO: Nur für Windows-Systeme
                                print(" --> Letze Bearbeitung: " + my_file.flt_modified_date.strftime ('%Y-%m-%d %H:%M:%S'))
                                print(" --> User ID: " + str(my_file.int_user_id))
                                print(" --> Group ID: " + str(my_file.int_group_id))
                                print(" --> MD5- Hash: " + str(my_file.str_hash_value_md5))
                                print(" --> Dateityp: " + str(my_file.str_extension))

                                str_query: str= "INSERT INTO `tbl_scan` (`id`, `job_id`, `path`, `file_name`, `extension`, `size`, `hash`, `user_id`, `group_id`, `filemode`, `created_date`, `modified_date`) "
                                str_query +="VALUES (NULL, NULL,'"+ my_file.str_path + "','"+ my_file.str_name+ "', '" + my_file.str_extension+ "', '"
                                str_query +=str(my_file.int_size) + "', '" + my_file.str_hash_value_md5 + "', '" + str(my_file.int_user_id) + "', '" + str(my_file.int_group_id)
                                str_query += "','" + my_file.str_filemode
                                str_query +="','" + my_file.flt_created_date.strftime ('%Y-%m-%d %H:%M:%S') + "','" + my_file.flt_modified_date.strftime ('%Y-%m-%d %H:%M:%S') + "')"

                                print(str_query)

                                sql_connector.writeData(str_query)

                sql_connector.commit()
                str_current_folder = next(iter(self._FolderList), None)

        flt_ts_end = datetime.timestamp(datetime.now())

        print("Anzahl der gescannten Verzeichnisse: " + str(int_dir_counter))
        print("Anzahl der gescannten Dateien: " + str(int_file_counter))
        print("Dauer der Ausführung: " + str( (flt_ts_end - flt_ts_start)) + " mics")

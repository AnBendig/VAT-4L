from datetime import datetime
import os
from model.DirectoryEntry import DirectoryEntry
from model.Entry import Entry
from model.Configuration import Configuration
from model.SQLConntect import SQLConnect
from model.Job import Job


class DirectoryScanner:
    """

    """

    def __init__(self, config: Configuration, sql_connector: SQLConnect , current_job: Job):
        #  Initialisierung der Attribute
        #if config is None:
        #    pass

        self._Config: Configuration = config
        self._sql_connector= sql_connector
        self._FolderList = []
        self._FolderList.append(self._Config.str_root_folder)
        self._currentJob: Job = current_job

    def startScan(self):

        #print("starte Scan...")

        int_file_counter: int = 0
        int_dir_counter:int =0

        if len(self._FolderList) > 0:
            str_current_folder = next(iter(self._FolderList), None)

            while str_current_folder is not None:
                with os.scandir(str_current_folder) as entries:
                    for entry in entries:
                        if entry.is_dir() and not entry.is_symlink():
                            my_dir: DirectoryEntry = DirectoryEntry(self._Config)
                            my_dir.readEntry(entry)

                            if not (my_dir.str_path in self._FolderList) :
                                self._FolderList.append(my_dir.str_path)

                                int_dir_counter +=1

                                """
                                print("Verzeichnis: " + my_dir.str_path)
                                print(" --> Erstellt am: " + my_dir.flt_created_date.strftime ('%Y-%m-%d %H:%M:%S'))  # TODO: Nur für Windows-Systeme
                                print(" --> Letze Bearbeitung: " + my_dir.flt_modified_date.strftime ('%Y-%m-%d %H:%M:%S'))
                                print(" --> User ID: " + str(my_dir.int_group_id))
                                print(" --> Group ID: " + str(my_dir.int_group_id))
                                """

                                str_query: str = "INSERT INTO `tbl_scan` (`id`, `job_id`, `is_directory`, `path`, `user_id`, `user_name`,`group_id`, `group_name`, `filemode`, `created_date`, `modified_date`) "
                                str_query += "VALUES (NULL, '" + str(self._currentJob.job_id) + "' ," + str(my_dir.bol_is_directory).upper() + ", '" + my_dir.str_path + "', '"
                                str_query += str(my_dir.int_user_id) + "', '" + my_dir.str_user_name + "', '"
                                str_query += str(my_dir.int_group_id) + "', '" + my_dir.str_group_name + "', '"
                                str_query += my_dir.str_filemode + "','"
                                str_query += my_dir.flt_created_date.strftime('%Y-%m-%d %H:%M:%S') + "','" + my_dir.flt_modified_date.strftime('%Y-%m-%d %H:%M:%S') + "')"

                                #print(str_query)

                                self._sql_connector.writeData(str_query)
                                
                                
                        else:
                            my_file: Entry = Entry(self._Config)

                            if not entry.is_symlink():
                                my_file.readEntry(entry)

                                int_file_counter +=1

                                """
                                print("Datei: " + my_file.str_name)
                                print(" --> Dateigröße: " + str(my_file.int_size) + " Bytes")
                                print(" --> Erstellt am: " + my_file.flt_created_date.strftime ('%Y-%m-%d %H:%M:%S'))  # TODO: Nur für Windows-Systeme
                                print(" --> Letze Bearbeitung: " + my_file.flt_modified_date.strftime ('%Y-%m-%d %H:%M:%S'))
                                print(" --> User ID: " + str(my_file.int_user_id))
                                print(" --> User Name: " + my_file.str_user_name)
                                print(" --> Group ID: " + str(my_file.int_group_id))
                                print(" --> Group Name: " + my_file.str_group_name)
                                print(" --> MD5- Hash: " + str(my_file.str_hash_value_md5))
                                print(" --> Dateityp: " + str(my_file.str_extension))
                                """

                                str_query: str= "INSERT INTO `tbl_scan` (`id`, `job_id`, `is_directory`, `path`, `file_name`, `extension`, `size`, `hash`, `user_id`, `user_name`,`group_id`, `group_name`, `filemode`, `created_date`, `modified_date`) "
                                str_query += "VALUES (NULL, '" + str(self._currentJob.job_id) + "', " + str(my_file.bol_is_directory).upper() + ", '"+ my_file.str_path + "','"+ my_file.str_name+ "', '" + my_file.str_extension+ "', '"
                                str_query += str(my_file.int_size) + "', '" + my_file.str_hash_value_md5 + "', '"
                                str_query += str(my_file.int_user_id) + "', '" + my_file.str_user_name + "', '"
                                str_query += str(my_file.int_group_id)+ "', '" + my_file.str_group_name + "', '"
                                str_query += my_file.str_filemode + "','"
                                str_query += my_file.flt_created_date.strftime ('%Y-%m-%d %H:%M:%S') + "','" + my_file.flt_modified_date.strftime ('%Y-%m-%d %H:%M:%S') + "')"

                                # print(str_query)

                                self._sql_connector.writeData(str_query)

                self._sql_connector.commit()
                self._FolderList.remove(str_current_folder)

                str_current_folder = next(iter(self._FolderList), None)
        self._currentJob.int_processed_dir= int_dir_counter
        self._currentJob.int_processed_file= int_file_counter

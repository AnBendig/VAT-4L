from datetime import datetime
import os
from model import DirectoryEntry
from model import Entry
from model import Configuration

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
        print("starte Scan...")

        int_file_counter: int = 0
        int_dir_counter:int =0

        if len(self._FolderList) > 0:
            str_current_folder = next(iter(self._FolderList), None)

            while str_current_folder is not None:
                self._FolderList.remove(str_current_folder)
                with os.scandir(str_current_folder) as entries:
                    for entry in entries:
                        if entry.is_dir():
                            my_dir: DirectoryEntry = DirectoryEntry.DirectoryEntry()
                            my_dir.readEntry(entry)

                            self._FolderList.append(my_dir.str_path)

                            int_dir_counter +=1
                            print("Verzeichnis: " + my_dir.str_path)
                            print(" --> Erstellt am: " + str(datetime.fromtimestamp(my_dir.flt_created_date)))  # TODO: Nur für Windows-Systeme
                            print(" --> Letze Bearbeitung: " + str(datetime.fromtimestamp(my_dir.flt_modified_date)))
                            print(" --> User ID: " + str(my_dir.int_group_id))
                            print(" --> Group ID: " + str(my_dir.int_group_id))

                        else:
                            my_file: Entry = Entry.Entry()

                            my_file.readEntry(entry)
                            int_file_counter +=1
                            print("Datei: " + my_file.str_name)
                            print(" --> Dateigröße: " + str(my_file.int_size) + " Bytes")
                            print(" --> Erstellt am: " + str(datetime.fromtimestamp(my_file.flt_created_date)))  # TODO: Nur für Windows-Systeme
                            print(" --> Letze Bearbeitung: " + str(datetime.fromtimestamp(my_file.flt_modified_date)))
                            print(" --> User ID: " + str(my_file.int_user_id))
                            print(" --> Group ID: " + str(my_file.int_group_id))
                            print(" --> MD5- Hash: " + str(my_file.str_hash_value_md5))
                            print(" --> Dateityp: " + str(my_file.str_extension))

                str_current_folder = next(iter(self._FolderList), None)


        print("Anzahl der gescannten Verzeichnisse: " + str(int_dir_counter))
        print("Anzahl der gescannten Dateien: " + str(int_file_counter))

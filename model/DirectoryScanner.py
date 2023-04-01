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

        with os.scandir(self._Config.str_root_folder) as entries:
            for entry in entries:
                if entry.is_dir():
                    my_dir: DirectoryEntry = DirectoryEntry.DirectoryEntry()

                    my_dir.readEntry(entry)

                    print("Verzeichnis: " + my_dir.str_path)
                    print(" --> Erstellt am: " + str(datetime.fromtimestamp(my_dir.flt_created_date)))  # TODO: Nur für Windows-Systeme
                    print(" --> Letze Bearbeitung: " + str(datetime.fromtimestamp(my_dir.flt_modified_date)))
                    print(" --> User ID: " + str(my_dir.int_group_id))
                    print(" --> Group ID: " + str(my_dir.int_group_id))

                else:
                    my_file: Entry = Entry.Entry()

                    my_file.readEntry(entry)

                    print("Datei: " + my_file.str_name)
                    print(" --> Dateigröße: " + str(my_file.int_size) + " Bytes")
                    print(" --> Erstellt am: " + str(datetime.fromtimestamp(my_file.flt_created_date)))  # TODO: Nur für Windows-Systeme
                    print(" --> Letze Bearbeitung: " + str(datetime.fromtimestamp(my_file.flt_modified_date)))
                    print(" --> User ID: " + str(my_file.int_user_id))
                    print(" --> Group ID: " + str(my_file.int_group_id))
                    print(" --> MD5- Hash: " + str(my_file.str_hash_value_md5))
                    print(" --> Dateityp: " + str(my_file.str_extension))



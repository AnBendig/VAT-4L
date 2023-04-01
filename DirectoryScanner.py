import datetime
import os
import hashlib

class DirectoryScanner:
    """

    """

    def __init__(self, Config):
        #  Initialisierung der Attribute
        if Config is None:
            pass

        self._Config = Config
        self._FolderList = []

        self._FolderList.append(self._Config.root_folder)

    def startScan(self):
        print("starte Scan...")
        myPath = "C:\\Users\\andreas.bendig\\OneDrive - bmsoft information technologies GmbH\\Dokumente"
        myFile: str = "todo.txt"

        """
        for root, dirs, files in os.walk("C:\\Users\\andreas.bendig\\OneDrive - bmsoft information technologies GmbH\\Dokumente"):
            for file in files:
                os.get file.
        """
        with os.scandir(myPath) as entries:
            for entry in entries:
                if entry.is_dir():
                    print("Verzeichnis: " + entry.path)
                else:
                    print("Datei: " + entry.name)
                    print(" --> Dateigröße: " + str(entry.stat().st_size) + " Bytes")
                    print(" --> Erstellt am: " + str(datetime.datetime.fromtimestamp(entry.stat().st_ctime)))  # TODO: Nur für Windows-Systeme
                    print(" --> Letze Bearbeitung: " + str(datetime.datetime.fromtimestamp(entry.stat().st_mtime)))
                    print(" --> User ID: " + str(entry.stat().st_uid))
                    print(" --> Group ID: " + str(entry.stat().st_gid))
                    print(" --> MD5- Hash: " + str(self._createHash(entry.path)))
                    print(" --> Dateityp: " + str(self._getFileType(entry.name)))

    def _createHash(self, filepath: str):
        hasher = hashlib.md5()
        with open( filepath, 'rb') as afile:
            buf = afile.read()
        hasher.update(buf)
        return hasher.hexdigest()

    def _getFileType(self, filename: str):
        strExtension: str = ""
        if filename.__contains__('.'):
            strExtension = os.path.splitext(filename)[1]

        return strExtension



class DirectoryScanner:
    """

    """

    def __init__(self, Config):
        #  Initialisierung der Attribute
        if Config is None:
            pass

        self._Config = Config
        self._RootFolder = self._Config["ROOT"]["path"]
        self._FolderList = []

        self._FolderList.append(self._RootFolder)

    def startScan(self):
        print("starte Scan...")



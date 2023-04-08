import hashlib
import os
from model.Entry import Entry
from model.Configuration import Configuration

class FileEntry(Entry):
    """
    Klasse zur Verwaltung von Datei-Informationen
    """
    def __init__(self, config: Configuration):
        """
        Erstellt ein Objekt der klasse.

        :param config:
            Configuration. Verwaltet die anwendungsspezifischen Parameter.
        """
        super().__init__(config)    # Laden des Konstruktors der Basisklasse Entry
        self.str_hash_value_md5: str = ""   # speichert den berechneten Hash-Wert einer Datei
        self.str_extension: str = ""        # enthält die Dateiendung (Dateityp)
        self.str_name: str = ""             # Name der Datei
        self.bol_is_directory: bool = False
        self.int_size: int = 0              # größe der Datei in Bytes

    def readEntry(self, entry: os.DirEntry):
        """
        Überschreibt die Methode der Basisklasse. Liest ein Verzeichniselement ein und weist die Inhalte den entsprechenden Attributen zu.

        :param entry:
            os.DirEntry. Das zu verarbeitende Verzeichniselement.
        :return:
            Keine Rückgabe.
        """
        super().readEntry(entry) # Methode der basisklasse ausführen

        if entry.is_file():
            # Verzeichniselement ist eine Datei
            self.bol_is_directory: bool = False
            self.str_hash_value_md5: str = str(self._createHash(entry.path))
            self.str_extension: str = str(self._getFileType(entry.name))
            self.str_name: str = entry.name
            self.int_size: int = entry.stat().st_size

    def _createHash(self, str_filepath: str) -> str:
        """
        Berechnet den Hash-Wert einer Datei

        :param filepath:
            String. Der Pfad zur Datei
        :return:
            String. Liefert den berechneten Hash-Wert der Datei.
                    Liefert "NoFile", falls es sich nicht um eine Datei handelt.
        """
        if self.str_extension in self._config.strs_ignore_extensions:
            return "noFile"

        my_hasher = hashlib.md5()
        with open( str_filepath, 'rb') as dat_file:
            buf = dat_file.read()
        my_hasher.update(buf)

        return my_hasher.hexdigest()

    def _getFileType(self, filename: str) -> str:
        """
        Liefert den Dateityp einer Datei. (alles nach dem ".")

        :param filename:
            String. Name der Datei.
        :return:
            String. Liefert die Dateiendung. Wenn keine gefunden wurde, wir "" zurückgegeben.
        """

        str_extension: str = ""

        if filename.__contains__('.'):
            # Dateiname enthält einen "."
            str_extension = os.path.splitext(filename)[1]

        return str_extension
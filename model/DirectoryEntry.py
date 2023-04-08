from os import DirEntry
from model.Entry import Entry
from model.Configuration import Configuration

class DirectoryEntry(Entry):
    """
    Die Klasse spezifiziert die Klasse 'Entry' und bildet die Eigenschaften und Methoden eines Verzeichnisses ab.
    """
    def __init__(self, config: Configuration):
        """
        Initialisiert ein Objekt dieser klasse
        :param config:
            Configuration. Verwaltung der Anwendungsparameter
        """
        super().__init__(config)
        self.bol_is_directory: bool = True

    def readEntry(self, entry: DirEntry):
        """Liest einen Verzeichniseintrag und analysiert diesen.
        Diese Methode überschreibt die der Elternklasse

        :param entry:
            Element aus der Verzeichnisstruktur. Kann ein Verzeichnis oder eine Datei sein.
        :return:
        Keine Rückgabe.
        """
        super().readEntry(entry)
        if entry.is_dir():
            self.bol_is_directory = True
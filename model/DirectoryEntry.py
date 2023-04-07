from os import DirEntry
from model.Entry import Entry
from model.Configuration import Configuration

class DirectoryEntry(Entry):
    def __init__(self, config: Configuration):
        super().__init__(config)
        self.bol_is_directory: bool = True

    def readEntry(self, entry: DirEntry):
        super().readEntry(entry)
        if entry.is_dir():
            self.bol_is_directory = True
import hashlib
import os
from model.Entry import Entry
from model.Configuration import Configuration

class FileEntry(Entry):

    def __init__(self, config: Configuration):
        super().__init__(config)
        self.str_hash_value_md5: str = ""
        self.str_extension: str = ""
        self.str_name: str = ""
        self.bol_is_directory: bool = False
        self.int_size: int = 0

    def readEntry(self, entry: os.DirEntry):
        super().readEntry(entry)
        if entry.is_file():
            self.bol_is_directory: bool = False
            self.str_hash_value_md5: str = str(self._createHash(entry.path))
            self.str_extension: str = str(self._getFileType(entry.name))
            self.str_name: str = entry.name
            self.int_size: int = entry.stat().st_size

    def _createHash(self, filepath: str):
        if self.str_extension in self._config.strs_ignore_extensions:
            return "noFile"

        hasher = hashlib.md5()
        with open( filepath, 'rb') as afile:
            buf = afile.read()
        hasher.update(buf)
        return hasher.hexdigest()

    def _getFileType(self, filename: str):
        str_extension: str = ""
        if filename.__contains__('.'):
            str_extension = os.path.splitext(filename)[1]

        return str_extension
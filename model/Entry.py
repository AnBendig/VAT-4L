import hashlib
import os

import model.Configuration
from model.DirectoryEntry import DirectoryEntry
from model.Configuration import Configuration

class Entry(DirectoryEntry):

    def __init__(self, config: Configuration):
        super().__init__(config)
        self.str_hash_value_md5: str = None
        self.str_extension: str = None
        self.str_name: str =None
        self.bol_isDirectory = False
        self.int_size: int = 0

    def readEntry(self, entry: os.DirEntry):
        super().readEntry(entry)
        self.str_hash_value_md5: str = str(self._createHash(entry.path))
        self.str_extension: str = str(self._getFileType(entry.name))
        self.str_name: str = entry.name
        self.int_size: int = entry.stat().st_size

    def _createHash(self, filepath: str):
        if self._config.strs_ignore_extensions.__contains__(self.str_extension):
        # if self.str_extension == ".sock" :
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
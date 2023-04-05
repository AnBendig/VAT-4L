import os
import stat
from datetime import datetime

from model.Configuration import Configuration

class DirectoryEntry:
    def __init__(self, config: Configuration):
        self._config: Configuration = config
        self.int_user_id: int = None
        self.flt_modified_date: datetime = None
        self.int_group_id: int = None
        self.flt_created_date: datetime = None
        self.str_path: str = ""
        self.bol_is_directory: bool = True
        self.str_filemode: str = ""

    def readEntry(self, entry: os.DirEntry):
        if not entry.is_symlink() :
            self.str_filemode: str =  stat.filemode(entry.stat().st_mode)
            self.str_path: str = entry.path.rstrip('/')
            self.int_user_id: int = entry.stat().st_uid
            self.int_group_id: int = entry.stat().st_gid
            self.flt_created_date: datetime = datetime.fromtimestamp(entry.stat().st_ctime)
            self.flt_modified_date: datetime = datetime.fromtimestamp(entry.stat().st_mtime)
        else:
            self.bol_is_directory: bool = False

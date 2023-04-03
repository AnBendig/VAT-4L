import os
from model.Configuration import Configuration

class DirectoryEntry:
    def __init__(self, config: Configuration):
        self._config: Configuration = config
        self.int_user_id: int = None
        self.flt_modified_date: float = 0
        self.int_group_id: int = None
        self.flt_created_date: float = 0
        self.str_path: str = None
        self.bol_is_directory: bool = True

    def readEntry(self, entry: os.DirEntry):
        if not entry.is_symlink() :
            self.str_path: str = entry.path
            self.int_user_id: int = entry.stat().st_uid
            self.int_group_id: int = entry.stat().st_gid
            self.flt_created_date: float = entry.stat().st_ctime
            self.flt_modified_date: float = entry.stat().st_mtime
        else:
            self.bol_is_directory: bool = False

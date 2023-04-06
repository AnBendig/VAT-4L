import os
import stat
from pwd import getpwuid
from grp import getgrgid

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
        self.str_user_name: str = ""
        self.str_group_name: str = ""

    def readEntry(self, entry: os.DirEntry):
        if not (entry.is_symlink()):
            self.str_filemode: str =  stat.filemode(entry.stat().st_mode)
            self.str_path: str = os.path.abspath(entry.path)
            self.int_user_id: int = entry.stat().st_uid
            self.int_group_id: int = entry.stat().st_gid
            self.str_user_name = getpwuid(os.stat(entry.path).st_uid).pw_name
            self.str_group_name = getgrgid(os.stat(entry.path).st_gid).gr_name
            self.flt_created_date: datetime = datetime.fromtimestamp(entry.stat().st_ctime)
            self.flt_modified_date: datetime = datetime.fromtimestamp(entry.stat().st_mtime)
        else:
            self.bol_is_directory: bool = False

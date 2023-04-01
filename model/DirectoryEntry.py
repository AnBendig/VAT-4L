import os
class DirectoryEntry:
    def __init__(self):
        self.int_user_id: int = None
        self.flt_modified_date: float = 0
        self.int_group_id: int = None
        self.flt_created_date: float = 0
        self.str_path: str = None
        self.bol_is_directory: bool = True

    def readEntry(self, entry: os.DirEntry):
        self.str_path: str = entry.path
        self.int_user_id: int = entry.stat().st_uid
        self.int_group_id: int = entry.stat().st_gid
        self.flt_created_date: float = entry.stat().st_ctime
        self.flt_modified_date: float = entry.stat().st_mtime


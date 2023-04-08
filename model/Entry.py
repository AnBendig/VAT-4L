from os import DirEntry,path,stat
from stat import filemode
from pwd import getpwuid
from grp import getgrgid
from datetime import datetime
from model.Configuration import Configuration

class Entry:
    """
    Basisklasse für die Klassen "DirectoryEntry" und "FileEntry"
    """
    def __init__(self, config: Configuration):
        """
        Erstellt ein Objekt der Klasse.
        :param config:
            Configuration. Verwaltung der anwendungsspezifischen Parameter
        """

        self._config: Configuration = config
        self.int_user_id: int = -1
        self.flt_modified_date: datetime = datetime(1,1,1,0,0,0)
        self.int_group_id: int = -1
        self.flt_created_date: datetime = datetime.now()
        self.str_path: str = ""
        self.bol_is_directory: bool = False
        self.str_filemode: str = ""
        self.str_user_name: str = ""
        self.str_group_name: str = ""
        self.str_hash_value_md5: str = ""
        self.str_extension: str = ""
        self.str_name: str = ""
        self.bol_is_directory: bool = False
        self.int_size: int = 0

    def readEntry(self, entry: DirEntry):
        """
        Liest die übergebenen Attribute aus einem Verzeichniselement aus.
        :param entry:
            os.DirEntry. Das zu bearbeitende Verzeichniselement
        :return:
            Keine Rückgabe.
        """
        if not (entry.is_symlink()):
            self.str_filemode: str = filemode(entry.stat().st_mode)
            self.str_path: str = path.abspath(entry.path)
            self.int_user_id: int = entry.stat().st_uid
            self.int_group_id: int = entry.stat().st_gid
            self.str_user_name = getpwuid(stat(entry.path).st_uid).pw_name
            self.str_group_name = getgrgid(stat(entry.path).st_gid).gr_name
            self.flt_created_date: datetime = datetime.fromtimestamp(entry.stat().st_ctime)
            self.flt_modified_date: datetime = datetime.fromtimestamp(entry.stat().st_mtime)
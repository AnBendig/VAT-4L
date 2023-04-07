import os
from model.DirectoryEntry import DirectoryEntry
from model.FileEntry import FileEntry
from model.Configuration import Configuration
from model.SQLConntect import SQLConnect,SQLQueryComposer,SQLQueryType
from model.Job import Job

class DirectoryScanner:
    """

    """

    def __init__(self, config: Configuration, sql_connector: SQLConnect , current_job: Job):
        self._Config: Configuration = config
        self._sql_connector= sql_connector
        self._FolderList = []
        self._FolderList.append(self._Config.str_root_folder)
        self._currentJob: Job = current_job

    def startScan(self):
        int_file_counter: int = 0
        int_dir_counter:int =0

        if len(self._FolderList) > 0:
            str_current_folder = next(iter(self._FolderList), None)

            while str_current_folder is not None:
                with os.scandir(str_current_folder) as entries:
                    for entry in entries:
                        if entry.is_dir() and not entry.is_symlink():
                            my_dir: DirectoryEntry = DirectoryEntry(self._Config)
                            my_dir.readEntry(entry)

                            if not (my_dir.str_path in self._FolderList) :
                                self._FolderList.append(my_dir.str_path)
                                int_dir_counter +=1
                                str_query = self._build_query(my_dir)

                                self._sql_connector.writeData(str_query)
                        else:
                            my_file: FileEntry = FileEntry(self._Config)

                            if not entry.is_symlink():
                                my_file.readEntry(entry)
                                int_file_counter +=1
                                str_query= self._build_query(my_file)

                                self._sql_connector.writeData(str_query)

                self._sql_connector.commit()
                self._FolderList.remove(str_current_folder)

                str_current_folder = next(iter(self._FolderList), None)
        self._currentJob.int_processed_dir= int_dir_counter
        self._currentJob.int_processed_file= int_file_counter

    def _build_query(self, current_entry) -> str:
        sql_composer: SQLQueryComposer = SQLQueryComposer()

        sql_composer.add("job_id", self._currentJob.job_id)
        sql_composer.add("is_directory", current_entry.bol_is_directory)
        sql_composer.add("path", current_entry.str_path)
        sql_composer.add("user_id", current_entry.int_user_id)
        sql_composer.add("user_name", current_entry.str_user_name)
        sql_composer.add("group_id", current_entry.int_group_id)
        sql_composer.add("group_name", current_entry.str_group_name)
        sql_composer.add("filemode", current_entry.str_filemode)
        sql_composer.add("created_date", current_entry.flt_created_date)
        sql_composer.add("modified_date", current_entry.flt_modified_date)

        if type(current_entry) is FileEntry:
            sql_composer.add("file_name", current_entry.str_name)
            sql_composer.add("extension", current_entry.str_extension)
            sql_composer.add("hash", current_entry.str_hash_value_md5)
            sql_composer.add("size", current_entry.int_size)

        str_query = sql_composer.get_query(SQLQueryType.INSERT, "tbl_scan")
        return str_query
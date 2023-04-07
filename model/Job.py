from datetime import datetime, timedelta
from model import SQLConntect
class Job():

    def __init__(self):
        self.job_id: int = 0
        self.dt_job_start: datetime = None
        self.dt_job_end: datetime = None
        self.int_job_duration = 0
        self.int_processed_dir: int = 0
        self.int_processed_file: int= 0

    def createJob(self):
        self.dt_job_start= datetime.now()

    def endJob(self, sql_connection: SQLConntect):
        self.dt_job_end = datetime.now()
        self.int_job_duration= self._get_runtime()

        str_query: str = "UPDATE `tbl_job` SET "
        str_query += "`dt_start_job`='"+ str(self.dt_job_start.strftime('%Y-%m-%d %H:%M:%S')) +"',"
        str_query += "`dt_end_job`='"+ str(self.dt_job_end.strftime('%Y-%m-%d %H:%M:%S')) +"',"
        str_query += "`int_processed_dir`='" + str(self.int_processed_dir) + "',"
        str_query += "`int_processed_file`='" + str(self.int_processed_file) + "' "
        str_query += "WHERE id_job= '" + str(self.job_id) + "'"

        sql_connection.writeData(str_query)
        sql_connection.commit()


    def create_job(self, sql_connection: SQLConntect):
        self.dt_job_start = datetime.now()
        str_query: str = "INSERT INTO `tbl_job` (`dt_start_job`) VALUES ('" + self.dt_job_start.strftime('%Y-%m-%d %H:%M:%S') + "')"
        sql_connection.writeData(str_query)
        self.job_id = sql_connection.get_last_row_id()
        sql_connection.commit()

    def _get_runtime(self) -> int:
        diff: timedelta = self.dt_job_end - self.dt_job_start
        return diff.microseconds
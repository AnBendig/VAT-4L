import mysql.connector
from model import Job
from datetime import datetime
class SQLConnect:

    def __init__(self):
        self._SQLConnection: mysql.connector.MySQLConnection = None
        self._bol_is_connected = False
        self._sql_cursor: mysql.connector.MySQLConnection.cursor = None

    def createConnection(self, str_server: str,str_port: str, str_user: str, str_password: str, str_database: str):
        try:
             self._SQLConnection= mysql.connector.connect(
                host=str_server,
                user=str_user,
                password= str_password,
                port= str_port,
                database= str_database)

        except:
            print("Verbindung konnte nicht hergestellt werden:")
            #  TODO: Make Log Entry

        else:
            if self._SQLConnection.is_connected():
                self._bol_is_connected = True
                self._sql_cursor= self._SQLConnection.cursor()

    def readData(self, str_query: str) -> dict:
        self._sql_cursor.execute(str_query)


    def writeData(self, str_query: str) -> bool:
        return self._sql_cursor.execute(str_query)

    def updateData(self, str_query: str) -> bool:
        pass

    def commit(self):
        self._SQLConnection.commit()

    def createJob(self)-> Job:
        job_new: Job = Job.Job()
        str_query: str = "INSERT INTO `tbl_job` (`dt_start_job`) VALUES ('" + datetime.now().strftime( '%Y-%m-%d %H:%M:%S' ) + "')"
        self._SQLConnection.cursor().execute(str_query)
        self._SQLConnection.cursor().getlastrowid()

        return job_new





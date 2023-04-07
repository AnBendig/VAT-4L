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
                self._sql_cursor: mysql.connector.MySQLConnection.cursor= self._SQLConnection.cursor()

    def readData(self, str_query: str) -> dict:
        self._sql_cursor.execute(str_query)


    def writeData(self, str_query: str) -> bool:
        return self._sql_cursor.execute(str_query)

    def updateData(self, str_query: str) -> bool:
        pass

    def commit(self):
        self._SQLConnection.commit()

    def get_last_row_id(self)-> int:
        self._sql_cursor.execute('SELECT LAST_INSERT_ID()')  # Add this
        int_last_row: int = int(self._sql_cursor.fetchone()[0]) # Add this

        return int_last_row








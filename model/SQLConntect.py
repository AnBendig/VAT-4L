from enum import Enum

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


class SQLQueryType(Enum):
    INSERT = 1
    UPDATE = 2
    SELECT = 3
    DELETE = 4

class SQLQueryComposer:
    def __init__(self):
        self.str_query : str= ""
        self.str_keylist: list = []
        self.str_valuelist: list = []


    def add(self, str_key: str, var_value):
        self.str_keylist.append(str_key)
        if type(var_value) is bool:
            self.str_valuelist.append(str(var_value).upper())
        elif type(var_value) is datetime:
            self.str_valuelist.append("'" + var_value.strftime('%Y-%m-%d %H:%M:%S') + "'")
        else:
            self.str_valuelist.append("'" + str(var_value) + "'")


    def _get_string(self,lst_content: list) -> str:
        return ", ".join(lst_content)


    def get_query(self, query_type: SQLQueryType, str_table_name : str):
        str_query: str = ""
        if query_type is SQLQueryType.INSERT:
            str_query = "INSERT INTO " + str_table_name + " (" + self._get_string(self.str_keylist) + ") "
            str_query += " VALUES (" + self._get_string(self.str_valuelist) + ")"

        return str_query



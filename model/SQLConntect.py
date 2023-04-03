import  .connector
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
            print("Verbindung konnte nicht hergestellt werden: " + x)
            #  TODO: Make Log Entry

        else:
            if self._SQLConnection.is_connected():
                self._bol_is_connected = True
                self._sql_cursor= self._SQLConnection.cursor()

    def readData(self, str_query: str) -> dict:
        self._sql_cursor.execute(str_query)


    def writeData(self, str_query: str) -> bool:
        self._sql_cursor.execute(str_query)

    def updateData(self, str_query: str) -> bool:
        pass

    def create_table(self, str_table_name: str, str_column):
        pass



from enum import Enum
import mysql.connector
from datetime import datetime
class SQLConnect:
    """
    Klasse stellt die Kommunikation zwischen der Anwendung und der Datenbank her. Sie stellt Methoden zur Abfrage und Speicherung von Anfragen bereit.
    Die Parameter für den Zugriff auf den Datenbankserver und die Datenbank werden in der Konfigurationsdatei verwaltet.
    """
    def __init__(self):
        """
        Erstellt ein Objekt dieser Klasse
        """
        self._SQLConnection: mysql.connector.MySQLConnection = None     # Die Verbindung zur Datenbank
        self._bol_is_connected = False                                  # Status der Verbindung
        self._sql_cursor: mysql.connector.MySQLConnection.cursor = None # Zuweisung des Zeigers für Datenbankoperationen

    def createConnection(self, str_server: str,str_port: str, str_user: str, str_password: str, str_database: str):
        """
        Stellt die Verbindung zum Datenbankserver her.

        :param str_server:
            String. URL zum Host
        :param str_port:
            String. Port für die Kommunikation (Standard 3306)
        :param str_user:
            String. Benutzername für den Datenbankzugriff
        :param str_password:
            String. Passwort für den Datenbankzugriff
        :param str_database:
            String. Name der Datenbank
        :return:
            Keine Rückgabe
        """
        try:
            # Versuche, Verbindung anhand der Parameter herzustellen
             self._SQLConnection= mysql.connector.connect(
                host=str_server,
                user=str_user,
                password= str_password,
                port= str_port,
                database= str_database)

        except Exception as ex:
            print("Verbindung zum Server konnte nicht hergestellt werden:" + getattr(ex,'msg'))
            #  TODO: Make Log Entry
            exit(1012)

        else:
            if self._SQLConnection.is_connected():
                # Verbindung wurde erfolgreich hergestellt
                self._bol_is_connected = True

            else:
                print("Verbindung zur Datenbank konnte nicht hergestellt werden:")
                #  TODO: Make Log Entry
                exit(1013)

    def set_cursor(self, dictionary: bool):
        """
        Legt den Focus der aktuellen Verbindung zur Verarbeitung fest.
        :param dictionary:
            Boolean. Gibt an, ob ein Dictionary als Rückgabe erzeugt wird oder nicht.
        :return:
        """

        self._sql_cursor: mysql.connector.MySQLConnection.cursor = self._SQLConnection.cursor(dictionary= dictionary)



    def readData(self, str_query: str) -> dict:
        """
        Nicht implemnentiert!
        :param str_query:
        :return:
        """

        my_dict: dict= {}
        self._sql_cursor.execute(str_query)
        my_dict = self._sql_cursor.fetchall()

        return my_dict

    def writeData(self, str_query: str) -> bool:
        """
        Überträgt Daten in die Datenbank durch Übermittlung einer SQL-Anfrage.
        :param str_query:
            String. SQL-Anweisung zur Verarbeitung der Daten
        :return:
            Boolean. Liefert 'True', wenn Ausführung erfolgreich durchgeführt wurde.
        """
        return self._sql_cursor.execute(str_query)

    def updateData(self, str_query: str) -> bool:
        """
        nicht implementiert!!
        :param str_query:
        :return:
        """
        pass

    def commit(self):
        """
        Speichert die übertragenen Daten in die Datenbank
        :return:
            Keine Rückgabe.
        """
        self._SQLConnection.commit()

    def get_last_row_id(self)-> int:
        """
        Liefert die zuletzt erstellte ID des verarbeiteten Datensatzes zurück.
        :return:
            Integer. ID des zuletzt gespeicherten Datensatzes.
        """
        self._sql_cursor.execute('SELECT LAST_INSERT_ID()')  # Add this
        int_last_row: int = int(self._sql_cursor.fetchone()[0]) # Add this

        return int_last_row


class SQLQueryType(Enum):
    """
    Klasse zur Unterscheidung der Anweisungsformen für die Anweisungen an die Datenbank
    """
    INSERT = 1
    UPDATE = 2
    SELECT = 3
    DELETE = 4

class SQLQueryComposer:
    """
    Klasse zur Generierung von SQL-Anfragen an die Datenbank.
    """
    def __init__(self):
        """
        Erstellt ein Objekt der Klasse.
        """
        self.str_query : str= ""            # Abfrage
        self.str_keylist: list = []         # Liste der Felder
        self.str_valuelist: list = []       # Liste der Werte


    def add(self, str_key: str, var_value):
        """
        Fügt ein Schlüssel-Wert Paar zur Liste hinzu.
        :param str_key:
            String. Der Spaltenname in der Tabelle
        :param var_value:
            Variant. Der Wert, der in die Tabellenspalte geschrieben werden soll.
        :return:
        """

        self.str_keylist.append(str_key)     # Fügt den Schlüssel zur bestehenden Liste hinzu

        """
        Überprüfen, welchen Datentyp der Spaltenwert besitzt. Anpassung des Inhalts an die 
        SQL- Anforderungen in Abhängigkeit des jeweiligen Datentyps.
        """
        if type(var_value) is bool:
            self.str_valuelist.append(str(var_value).upper())

        elif type(var_value) is datetime:
            self.str_valuelist.append("'" + var_value.strftime('%Y-%m-%d %H:%M:%S') + "'")

        else:
            self.str_valuelist.append("'" + str(var_value) + "'")


    @staticmethod
    def _get_string(lst_content: list) -> str:
        """
        Fügt die Elemente eine Liste zu einer Zeichenkette zusammen. Die Elemente werden
        durch ", " verbunden.
        :param lst_content:
            List. Die zu bearbeitende Liste
        :return:
            String. Beinhaltet die erstellte Zeichenkette.
        """
        return ", ".join(lst_content)


    def get_query(self, query_type: SQLQueryType, str_table_name : str) -> str:
        """
        Die Methode erstellt anhand des Anfragetyps die SQL-Anweisung.
        :param query_type:
            SQLQueryType. Typ der Anfrage
        :param str_table_name:
            String. Name der Tabelle in der Datenbank.
        :return:
            String. Liefert die generierte SQL-Abfrage zurück
        """
        str_query: str = ""
        if query_type is SQLQueryType.INSERT:
            str_query = "INSERT INTO " + str_table_name + " (" + self._get_string(self.str_keylist) + ") "
            str_query += " VALUES (" + self._get_string(self.str_valuelist) + ")"

        return str_query



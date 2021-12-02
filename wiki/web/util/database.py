from flask import current_app
from .singleton import Singleton
import pyodbc


class Database(Singleton):
    def __init__(self):
        """
        Initializes an instance of the Database with a connection to the database.
        """
        self._conn = pyodbc.connect(current_app.config['CONNECTION_STRING'])

    def execute_query_for_result(self, query) -> list:
        """
        Executes a query where a result is expected (SELECT statements).

        :param query: The query to be executed.

        :return: A dictionary of the results from the query. None if an error occured.
        """
        try:
            cursor = self._conn.execute(query)

            columns = [column[0] for column in cursor.description]
            records = [dict(zip(columns, row)) for row in cursor.fetchall()]

            return records
        except:
            return None

    def execute_query(self, query) -> bool:
        """
        Executes a query where no result is expected (INSERT, UPDATE, and DELETE statements).

        :param query: The query to be executed.

        :return: True if the query completed without errors, false otherwise.
        """
        try:
            self._conn.execute(query).commit()
            return True
        except:
            return False

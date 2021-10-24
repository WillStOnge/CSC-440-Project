"""
    Database Manager
    ~~~~~~~~~~~~~~~~~~~~~~
"""
from flask import current_app
import pyodbc


class Database:
    def __init__(self):
        self._conn = pyodbc.connect(current_app.config['CONNECTION_STRING'])


    def getCursor(self) -> pyodbc.Cursor:
        """
        Returns a cursor which can be used to execute SQL statements.
        """
        return self._conn.cursor()

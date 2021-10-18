"""
    Database Manager
    ~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import current_app
import pyodbc

class Database:
    def __init__(self):
        self._conn = pyodbc.connect(current_app.config['CONNECTION_STRING'])

    def getConnection(self):
        return self._conn

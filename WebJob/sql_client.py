import os
import pyodbc


"""
Connects to the SQL database like /CourseGrab/models/sql_client.py, but
files are separate since WebJob files are uploaded as a zip file.

Checks subscribed courses for any changes in availability.
"""
class Client(object):
    def __init__(self):
        server = "tcp:coursegrabdb.database.windows.net"
        database = "coursegrabdb"   
        username = "nnsun"
        password = os.getenv("DB_PASSWORD")
        self.connection = pyodbc.connect("DRIVER={ODBC Driver 13 for SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s"
                            % (server, database, username, password))
        self.cursor = self.connection.cursor()

    
    def poll_courses(self):
        """Returns a list of subscribed course numbers that correspond to newly open courses"""
        command = "SELECT DISTINCT CourseNum FROM Users"
        self.cursor.execute(command)
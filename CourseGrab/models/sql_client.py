import os
import pyodbc

class Client(object):
    def __init__(self):
        server = "tcp:coursegrabdb.database.windows.net"
        database = "coursegrabdb"   
        username = "nnsun"
        password = os.getenv("EMAIL_PASSWORD")
        self.connection = pyodbc.connect("DRIVER={ODBC Driver 13 for SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s"
                            % (server, database, username, password))
        self.cursor = self.connection.cursor()
    
    def create_user(self, name, email, password, phone_number, send_email):
        command = "INSERT INTO Users(Name, Email, Password, PhoneNumber, SendEmail) VALUES (?, ?, ?, ,?, ?, 0)"
        values = [name, email, phone_number, password, send_email]
        self.cursor.execute(command, values)
        self.connection.commit()
        self.connection.close()

    def submit_request(self, email, course_code):
        command = "INSERT INTO NotifierMap(Email, CourseNumber) VALUES (?, ?)"
        values = [email, course_code]
        self.cursor.execute(command, values)
        self.connection.commit()
        self.connection.close()

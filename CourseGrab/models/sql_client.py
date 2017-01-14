import os
import pyodbc

class Client(object):
    def __init__(self):
        server = "tcp:coursegrabdb.database.windows.net"
        database = "coursegrabdb"   
        username = "nnsun"
        password = os.getenv("DB_PASSWORD")
        self.connection = pyodbc.connect("DRIVER={ODBC Driver 13 for SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s"
                            % (server, database, username, password))
        self.cursor = self.connection.cursor()


    def add_course(self, course_num, subject_code):
        command = "INSERT INTO Courses (CourseNum, SubjectCode, SendStatus) VALUES (?, ?, 1)"
        values = [course_num, subject_code]
        self.cursor.execute(command, values)
        self.cursor.commit()

    
    def create_user(self, name, email, password, phone_number, send_email):
        command = "INSERT INTO Users (Name, Email, Password, PhoneNumber, SendEmail) VALUES (?, ?, ?, ,?, ?, 0)"
        values = [name, email, phone_number, password, send_email]
        self.cursor.execute(command, values)
        self.connection.commit()


    def submit_request(self, email, course_number):
        command = "SELECT * FROM Users WHERE Email = ?"
        self.cursor.execute(command, email)
        row = self.cursor.fetchone();
        if row is None:
            command = "INSERT INTO Users (Email, Subscription_1, TrackStatus_1) VALUES (?, ?, 1)"
            self.cursor.execute(command, email, course_number)
        elif row.Subscription_1 is None:
            command = "UPDATE Users SET Subscription_1 = ?, TrackStatus_1 = 1"
            self.cursor.execute(command, course_number)
        elif row.Subscription_2 is None:
            command = "UPDATE Users SET Subscription_2 = ?, TrackStatus_2 = 1"
            self.cursor.execute(command, course_number)
        elif row.Subscription_3 is None:
            command = "UPDATE Users SET Subscription_3 = ?, TrackStatus_2 = 1"
            self.cursor.execute(command, course_number)
        else:
            raise UserWarning("User can not track more than three courses at a time.")
        self.connection.commit()

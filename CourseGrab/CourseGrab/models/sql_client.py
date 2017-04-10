import pyodbc
import os
import datetime
import pytz


class Client(object):
    def __init__(self):
        server = os.getenv("DB_SERVER")
        database = os.getenv("DB_NAME")
        username = os.getenv("DB_USERNAME")
        password = os.getenv("DB_PASSWORD")
        self.connection = pyodbc.connect("DRIVER={ODBC Driver 13 for SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s"
                            % (server, database, username, password))
        self.cursor = self.connection.cursor()


    def add_user(self, id, email):
        est = pytz.timezone("America/New_York")
        time = pytz.utc.localize(datetime.datetime.now(), is_dst=None).astimezone(est)
        command = "SELECT * FROM Users WHERE UserID = ?"
        self.cursor.execute(command, id)
        if self.cursor.fetchone() is None:
            print datetime.datetime.now()
            command = "INSERT INTO Users(UserID, Email, JoinedDatetime) VALUES (?, ?, ?)"
            self.cursor.execute(command, [id, email, time])
            self.cursor.commit()


    def get_courses(self, id):
        command = "SELECT Subscription_1, Subscription_2, Subscription_3 FROM Users WHERE UserID = ?"
        self.cursor.execute(command, id)
        courses = self.cursor.fetchone()
        if courses is None:
            return []
        courses = [x for x in courses if x is not None]
        if len(courses) == 0:
            return []
        courses_paren = "(%s)" % str(courses)[1:-1:]
        command = "SELECT Title, Section FROM Courses WHERE CourseNum IN %s" % courses_paren
        self.cursor.execute(command)
        titles = []
        sections = []
        row = self.cursor.fetchone()
        while row is not None:
            titles.append(row.Title)
            sections.append(row.Section)
            row = self.cursor.fetchone()
        course_list = []
        for i in xrange(len(courses)):
            course_list.append((courses[i], titles[i], sections[i]))
        return course_list


    def submit_request(self, id, course_num):
        command = "SELECT * FROM Courses WHERE CourseNum = ?"
        self.cursor.execute(command, course_num)
        row = self.cursor.fetchone()
        if row is None: 
            raise UserWarning("This course number does not exist.")
        
        command = "SELECT * FROM Subscriptions WHERE UserID = ? AND CourseNum = ?"
        self.cursor.execute(command, [id, course_num])
        if self.cursor.fetchone() is not None:
            raise UserWarning("You are already tracking this course.")

        command = "SELECT COUNT(*) as num_subs FROM Subscriptions WHERE UserID = ?"
        self.cursor.execute(command, id)
        row = self.cursor.fetchone()
        if row.num_subs == 3:
            raise UserWarning("You cannot track more than three courses at a time.")

        command = "INSERT INTO Subscriptions VALUES (?, ?)"
        self.cursor.execute(command, id, course_num)
        self.cursor.commit()


    def remove_course(self, id, course_num):
        command = "DELETE FROM Subscriptions WHERE UserID = ? AND CourseNum = ?"
        self.cursor.execute(command, id, course_num)
        self.cursor.commit()

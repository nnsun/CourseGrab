import check_course
import sys
sys.path.append("site-packages")
import send_email
from sql_client import Client


client = Client()
course_nums = set()
tracked_courses = set()

"""Create a list of tuples of subscribed course numbers and their respective subject codes"""
client.cursor.execute("SELECT DISTINCT Subscription_1 FROM Users")
row = client.cursor.fetchone()
while row is not None and row.Subscription_1 is not None:
    course_nums.add(row.Subscription_1)
    row = client.cursor.fetchone()

client.cursor.execute("SELECT DISTINCT Subscription_2 FROM Users")
row = client.cursor.fetchone()
while row is not None and row.Subscription_2 is not None:
    course_nums.add(row.Subscription_2)
    row = client.cursor.fetchone()

client.cursor.execute("SELECT DISTINCT Subscription_3 FROM Users")
row = client.cursor.fetchone()
while row is not None and row.Subscription_3 is not None:
    course_nums.add(row.Subscription_3)
    row = client.cursor.fetchone()

for course_num in course_nums:
    client.cursor.execute("SELECT SubjectCode FROM Courses WHERE CourseNum = ?", course_num)
    subject_code = client.cursor.fetchone().SubjectCode
    tracked_courses.add((course_num, subject_code))

tracked_courses = list(tracked_courses)

"""Sort the tracked courses into ones that are open and ones that are full"""
open_courses = []
closed_courses = []
for course in tracked_courses:
    if check_course.check(course[0], course[1]):
        open_courses.append(course[0])
    else:
        closed_courses.append(course[0])

for course_num in open_courses:
    client.cursor.execute("UPDATE Courses SET CheckStatus = 1 WHERE CourseNum = ?", course_num)
        
    client.cursor.execute("SELECT Email FROM Users where Subscription_1 = ? AND TrackStatus_1 = 1", course_num)
    email = client.cursor.fetchone()
    while email is not None:
        send_email.send(email, course_num)
        email = client.cursor.fetchone()
    client.cursor.execute("UPDATE Users SET TrackStatus_1 = 0 WHERE Subscription_1 = ?", course_num)
        
    client.cursor.execute("SELECT Email FROM Users where Subscription_2 = ? AND TrackStatus_2 = 1", course_num)
    email = client.cursor.fetchone()
    while email is not None:
        send_email.send(email, course_num)
        email = client.cursor.fetchone()
    client.cursor.execute("UPDATE Users SET TrackStatus_2 = 0 WHERE Subscription_2 = ?", course_num)

    client.cursor.execute("SELECT Email FROM Users where Subscription_3 = ? AND TrackStatus_3 = 1", course_num)
    email = client.cursor.fetchone()
    while email is not None:
        send_email.send(email, course_num)
        email = client.cursor.fetchone()
    client.cursor.execute("UPDATE Users SET TrackStatus_3 = 0 WHERE Subscription_3 = ?", course_num)

for course_num in closed_courses:
    client.cursor.execute("UPDATE Courses SET CheckStatus = 0 WHERE CourseNum = ?", course_num)
    client.cursor.execute("UPDATE Users SET TrackStatus_1 = 1 WHERE Subscription_1 = ?", course_num)
    client.cursor.execute("UPDATE Users SET TrackStatus_2 = 1 WHERE Subscription_2 = ?", course_num)
    client.cursor.execute("UPDATE Users SET TrackStatus_3 = 1 WHERE Subscription_3 = ?", course_num)

client.cursor.commit()
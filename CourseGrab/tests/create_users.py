from CourseGrab.models.sql_client import Client


"""Inserts 500 test users with random course subscriptions into the Users database.
Tests performance of querying course and user status."""

client = Client()
course_list = []

command = "SELECT TOP 1500 CourseNum FROM Courses"
client.cursor.execute(command)
row = client.cursor.fetchone()
while row is not None:
    course_list.append(row.CourseNum)
    row = client.cursor.fetchone()

for i in xrange(500):
    command = "INSERT INTO Users (UserID, Email, Subscription_1, TrackStatus_1) VALUES (?, ?, ?, 1)"
    user_id = str(int('1' + '0' * 20) + i)
    email = "test%d@example.com" % i
    subscription = course_list.pop()
    client.cursor.execute(command, [user_id, email, subscription])

client.cursor.commit()
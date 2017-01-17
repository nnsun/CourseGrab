import smtplib
import os


"""
Sends an email to email_address notifying the user that course_code is now open
"""
def send(email_address, course_code):
    smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    # read email password from email_password.txt (not uploaded to source control)
    password = os.getenv("EMAIL_PASSWORD")
    smtpObj.login("cornellcoursegrab@gmail.com", password)
    smtpObj.sendmail("cornellcoursegrab@gmail.com", email_address, "Subject: Course number %s is now open!\n" % course_code)
    smtpObj.quit()

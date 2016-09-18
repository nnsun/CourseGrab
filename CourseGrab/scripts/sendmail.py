import smtplib
from email.mime.text import MIMEText

def send_email(email_address, course_code):
    msg = MIMEText("Course number %s is now open!" % course_code)

    msg["Subject"] = msg
    msg["From"] = "ys395@cornell.edu"
    msg["To"] = email_address

    s = smtplib.SMTP('localhost')
    s.sendmail(me, [you], msg.as_string())
    s.quit()
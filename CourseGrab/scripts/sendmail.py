import smtplib

def send_email(email_address, course_code):
    smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login("cornellcoursegrab@gmail.com", "coursegrab")
    smtpObj.sendmail("cornellcoursegrab@gmail.com", "nsun200@live.com", "Subject: Course number %s is now open!\n" % course_code)
    smtpObj.quit()

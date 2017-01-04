import smtplib


"""
Sends an email to email_address notifying the user that course_code is now open
"""
def send(email_address, course_code):
    smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    # read email password from email_password.txt (not uploaded to source control)
    with open("email_password.txt", 'rU') as password_file:
        password = password_file.read()
    smtpObj.login("cornellcoursegrab@gmail.com", password)
    smtpObj.sendmail("cornellcoursegrab@gmail.com", email_address, "Subject: Course number %s is now open!\n" % course_code)
    smtpObj.quit()

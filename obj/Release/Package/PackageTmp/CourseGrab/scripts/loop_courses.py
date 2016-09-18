import check_course
import sendmail


def course_check(email_address, code):
    if check_course(code):
        sendmail.send_email(email_address, code)
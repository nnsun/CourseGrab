import check_course
import read_dict
import sendmail


def course_check(email_address, code):
    course_map = read_dict.read_dict()
    if check_course(code):
        sendmail.send_email(email_address, code)
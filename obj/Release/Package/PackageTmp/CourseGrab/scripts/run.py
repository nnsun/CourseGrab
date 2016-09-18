import check_course
import sendmail
import csv


with open("CourseGrab/scripts/ledger.csv", 'rU') as codes:
    code_reader = csv.reader(codes)
    code_reader.next()
    while True:
        try:
            code_line = code_reader.next()
            email = code_line[0]
            code = code_line[1]
            if check_course(code):
                sendmail.send_email(email_address, code)
        except StopIteration:
            break
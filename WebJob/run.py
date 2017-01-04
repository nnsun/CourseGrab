import check_course
import sys
sys.path.append("site-packages")
import send_email
import csv
import read_dict


"""
Iterates through the database and sends emails to users subscribed
to newly opened courses
"""
with open("ledger.csv", 'rU') as codes:
    code_reader = csv.reader(codes)
    while True:
        try:
            code_line = code_reader.next()
            email = code_line[0]
            code = code_line[1]
            if check_course.check_course(code):
                send_email.send(email, code)
        except StopIteration:
            break

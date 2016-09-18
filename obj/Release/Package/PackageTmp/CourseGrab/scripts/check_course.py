import sys
import requests
import bs4
import csv
import smtplib


def check_course(code):
    course_map = {}
    with open("CourseGrab/scripts/course_subject_dict.csv", 'rU') as dict_file:
        dict_reader = csv.reader(dict_file)
        while True:
            try:
                dict_line = dict_reader.next()
                course_map[int(dict_line[0])] = dict_line[1]
            except StopIteration:
                break
    subject = course_map[code]
    subject_page = requests.get("http://classes.cornell.edu/browse/roster/FA16/subject/" + subject)
    subject_page.raise_for_status()
    subject_bs4 = bs4.BeautifulSoup(subject_page.text, "lxml")
    course_code_tags = subject_bs4.find_all("strong", class_="tooltip-iws")
    for tag in course_code_tags:
        course_code = int(tag.getText().strip())
        if code == course_code:
            section = tag.parent.parent.parent
            if "open-status-open" in str(section):
                return True
            return False


def read_dict():
    course_map = {}
    with open("CourseGrab/scripts/course_subject_dict.csv", 'rU') as dict_file:
        dict_reader = csv.reader(dict_file)
        while True:
            try:
                dict_line = dict_reader.next()
                course_map[int(dict_line[0])] = dict_line[1]
            except StopIteration:
                break
    return course_map

def send_email(email_address, course_code):
    smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login("cornellcoursegrab@gmail.com", "coursegrab")
    smtpObj.sendmail("cornellcoursegrab@gmail.com", email_address, "Subject: Course number %s is now open!\n" % course_code)
    smtpObj.quit()


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

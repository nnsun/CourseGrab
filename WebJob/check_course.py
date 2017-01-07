import sys
import requests
import bs4
import csv
import pyodbc


"""
Returns True if the the the given course code is open, False otherwise. 
"""
def check_course(course_num, subject_code):
    subject_page = requests.get("http://classes.cornell.edu/browse/roster/SP17/subject/" + subject_code)
    subject_page.raise_for_status()
    subject_bs4 = bs4.BeautifulSoup(subject_page.text, "html.parser")
    course_code_tags = subject_bs4.find_all("strong", class_="tooltip-iws")
    for tag in course_code_tags:
        course_code = int(tag.getText().strip())
        if course_num == course_code:
            section = tag.parent.parent.parent
            if "open-status-open" in str(section):
                return True
            return False

import requests
import bs4
from CourseGrab.models.sql_client import Client


"""
Parses the Cornell class roster and builds a SQL database of all courses
"""
def main():
    client = Client()
    course_num_map = {}
    roster_page = "https://classes.cornell.edu/browse/roster/SP17"
    roster_request = requests.get(roster_page)
    roster_request.raise_for_status()
    roster_bs4 = bs4.BeautifulSoup(roster_request.text, "html.parser")
    subject_tags = roster_bs4.select(".browse-subjectcode")

    subject_list = []
    for tag in subject_tags:
        subject_list.append(str(tag.getText()))

    subjects_page = "https://classes.cornell.edu/browse/roster/SP17/subject/"
    for subject_code in subject_list:
        print subject_code
        subject_request = requests.get(subjects_page + subject_code)
        subject_bs4 = bs4.BeautifulSoup(subject_request.text, "html.parser")
        course_code_tags = subject_bs4.find_all("strong", class_ = "tooltip-iws")
        for tag in course_code_tags:
            course_num = int(tag.getText().strip())
            catalog_num = int("".join([x for x in tag.next_sibling.getText() if x.isdigit()]))
            title = tag.parent.parent.parent.parent.parent.parent.find_all("div", class_ = "title-coursedescr")[0].getText()
            section = str(tag.parent.parent.parent["aria-label"])[14:]
            command = "INSERT INTO Courses (CourseNum, OpenStatus, SubjectCode, CatalogNum, Title, Section) VALUES (?, 0, ?, ?, ?, ?)"
            client.cursor.execute(command, [course_num, subject_code, catalog_num, title, section])
    client.connection.commit()
    client.connection.close()

if __name__ == "__main__":
    main()

import requests
import bs4


def main():
    course_num_map = {}

    roster_page = requests.get("https://classes.cornell.edu/browse/roster/FA16")
    roster_page.raise_for_status()
    roster_bs4 = bs4.BeautifulSoup(roster_page.text, "lxml")
    subject_tags = roster_bs4.select(".acadgroup-subjectcode")

    subject_list = []
    for tag in subject_tags:
        subject_list.append(str(tag.getText()))

    for subject in subject_list:
        print subject
        subject_page = requests.get("http://classes.cornell.edu/browse/roster/FA16/subject/" + subject)
        subject_bs4 = bs4.BeautifulSoup(subject_page.text, "lxml")
        course_code_tags = subject_bs4.find_all("strong", class_="tooltip-iws")
        for tag in course_code_tags:
            course_code = int(tag.getText().strip())
            course_num_map[course_code] = subject

    map_file = open("course_subject_dict.csv", 'w')
    for key, value in course_num_map.iteritems():
        map_file.write("%d,%s\n" % (key, value))

if __name__ == "__main__":
    main()

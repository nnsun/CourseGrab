import csv


course_map = {}
with open("course_subject_dict.csv", 'rU') as dict_file:
    dict_reader = csv.reader(dict_file)
    while True:
        try:
            dict_line = dict_reader.next()
            course_map[int(dict_line[0])] = dict_line[1]
        except StopIteration:
            break

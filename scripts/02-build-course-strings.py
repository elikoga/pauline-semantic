#!/usr/bin/env python3

# use data/courses_extracted.json

import json

with open("data/courses_extracted.json") as f:
    courses_extracted = json.load(f)

course_strings = {}

# for each of the courses, we build a description string
for course in courses_extracted:
    description = ""
    # description += course["semester"] + "; "
    # description += course["cid"] + ": "
    description += course["name"] + "\n"
    if "ou" in course:
        description += "Fakultät: " + course["ou"] + "\n"
    if "instructors" in course:
        description += "Dozenten: " + course["instructors"] + "\n"
    if "small_groups" in course:
        description += "Kleingruppen: " + ", ".join(course["small_groups"]) + "\n"
    course_strings[course["cid"]] = description

# write the data to data/course_strings.json
with open("data/course_strings.json", "w") as f:
    json.dump(course_strings, f, indent=4)

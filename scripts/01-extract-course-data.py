#!/usr/bin/env python3

# use data/courses.json

import json

with open("data/courses.json") as f:
    courses = json.load(f)

# for each of the courses, collect semester, cid, name, ou (if not null), instructors (if not null), and small_groups[].name

all_courses = []

for semester in courses:
    for course in courses[semester]:
        cid = course["cid"]
        name = course["name"]
        ou = course["ou"] if "ou" in course else None
        instructors = course["instructors"] if "instructors" in course else None
        small_groups_names = (
            [sg["name"] for sg in course["small_groups"]]
            if "small_groups" in course
            else None
        )
        the_course = {
            "semester": semester,
            "cid": cid,
            "name": name,
        }
        if ou:
            the_course["ou"] = ou
        if instructors:
            the_course["instructors"] = instructors
        if small_groups_names:
            the_course["small_groups"] = small_groups_names
        all_courses.append(the_course)

# write the data to data/courses_extracted.json

with open("data/courses_extracted.json", "w") as f:
    json.dump(all_courses, f, indent=4)

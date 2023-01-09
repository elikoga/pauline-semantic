#!/usr/bin/env python3

# from https://pauline-upb.de/api/v1/<stuff>

import httpx
import asyncio
from tqdm import tqdm

# Get semesters/newest
API_BASE = "https://pauline-upb.de/api/v1"

# newest_semesters = requests.get(API_BASE + "/semesters/newest").json()
newest_semesters = httpx.get(API_BASE + "/semesters/newest").json()

# format is [{'name': 'Sommer 2022', 'created': '2022-04-06T14:13:52.746038', 'id': 3}, {'name': 'Winter 2022/23', 'created': '2022-10-03T22:17:39.839229', 'id': 7}]

# Get courses for all semesters

courses = {}

for semester in tqdm(newest_semesters):
    # get courses/all with url parameter of semesterId
    courses_for_semester = httpx.get(
        API_BASE + "/courses/all", params={"semesterId": semester["id"]}
    ).json()
    courses[semester["name"]] = courses_for_semester

    # Is in format:
    # [
    #   {
    #     "cid": "L.079.05401",
    #     "name": "Systemsoftware und systemnahe Programmierung",
    #     "description": ""
    #   }
    # ]

    # For each of the courses, get the course details with courses/{courseId}
    # And merge them into the courses dict
    for course in tqdm(courses_for_semester):
        course_details = httpx.get(
            API_BASE + "/courses/" + course["cid"],
            params={"semesterId": semester["id"]},
        ).json()
        course.update(course_details)
    # async def get_course_details(course, client):
    #     course_details = await client.get(
    #         API_BASE + "/courses/" + course["cid"],
    #         params={"semesterId": semester["id"]},
    #     )
    #     course.update(course_details.json())

    # async def call_courses():
    #     async with httpx.AsyncClient() as client:
    #         await asyncio.gather(
    #             *[get_course_details(course, client) for course in courses_for_semester]
    #         )

    # asyncio.run(call_courses())


# Now we have a dict with all the courses for all semesters
# Save into data/
import json

# Create data/ if it doesn't exist
import os

if not os.path.exists("data"):
    os.makedirs("data")

with open("data/courses.json", "w") as f:
    json.dump(courses, f, indent=4)

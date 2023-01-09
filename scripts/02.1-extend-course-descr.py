#!/usr/bin/env python3

# use data/courses_extracted.json

import json
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import json
from tqdm import tqdm

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


tokenizer = AutoTokenizer.from_pretrained("distilgpt2")

model = AutoModelForCausalLM.from_pretrained("distilgpt2")

generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

result = tqdm(
    generator(
        (s + "\nBeschreibung: " for s in course_strings.values()),
        max_new_tokens=50,
        do_sample=True,
    ),
    total=len(course_strings),
)

result = list(result)

# fuse result with cid
new_course_strings = {}
for idx, (cid, course_string) in enumerate(course_strings.items()):
    new_course_strings[cid] = result[idx]["generated_text"]

# write the data to data/course_strings_extended.json
with open("data/course_strings_extended.json", "w") as f:
    json.dump(new_course_strings, f, indent=4)

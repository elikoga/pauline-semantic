#!/usr/bin/env python3

import json
import sentence_transformers
from tqdm import tqdm
import pickle

with open("data/course_strings.json") as f:
    course_strings = json.load(f)

# embed the course descriptions using the sentence-transformers library

model = sentence_transformers.SentenceTransformer(
    # "sentence-transformers/all-MiniLM-L6-v2"
    "T-Systems-onsite/cross-en-de-roberta-sentence-transformer"
)

embeddings = {}

for cid, description in tqdm(course_strings.items()):
    embeddings[cid] = model.encode(description)

# write the data to data/embeddings.pickle

with open("data/embeddings.pickle", "wb") as f:
    pickle.dump(embeddings, f)

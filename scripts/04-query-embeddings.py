#!/usr/bin/env python3
import time

print(f"Start at time {time.time()}")

import json
import pickle
from sentence_transformers import SentenceTransformer, util
import sys
import typing
import numpy

print(f"Done importing at time {time.time()}")

with open("data/embeddings.pickle", "rb") as f:
    embeddings: dict[str, typing.Any] = pickle.load(f)

print(f"Loaded embeddings at time {time.time()}")

# model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
model = SentenceTransformer("T-Systems-onsite/cross-en-de-roberta-sentence-transformer")

print(f"Loaded model at time {time.time()}")

while True:
    # get query from user
    query = input("Enter query: ")
    k = int(input("Enter k: "))
    # load query from args
    # query = sys.argv[1]

    # embed query
    query_embedding = model.encode(query)

    print(f"Encoded query at time {time.time()}")

    # find the k most similar courses

    # k = 3942
    # k = 100

    # compute similarity scores of the query against all courses
    cosine_scores = util.pytorch_cos_sim(query_embedding, list(embeddings.values()))

    # get the k most similar courses using topk
    k_most_similar = cosine_scores.topk(k=k, largest=True)

    # get the indices of the k most similar courses
    k_most_similar_indices = k_most_similar.indices.flatten().tolist()

    print(f"Found k most similar at time {time.time()}")

    # get the k most similar courses
    k_most_similar_courses = [
        list(embeddings.keys())[i] for i in k_most_similar_indices
    ]

    # find course in course_strings.json
    with open("data/course_strings.json") as f:
        course_strings = json.load(f)

    # print the k most similar courses
    for idx, course in enumerate(k_most_similar_courses):
        course_string = course_strings[course]
        print(
            f"TOP{idx + 1} Similarity score: {cosine_scores[0][k_most_similar_indices[0]]}"
        )
        print(f"CID: {course}: {course_string}")

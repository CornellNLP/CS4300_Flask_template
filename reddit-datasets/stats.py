import json
import matplotlib.pyplot as plt
import numpy as np
import statistics

"""
used to use the finalized dataset to come up with meaningful statistics, like
word averages, etc
"""

file_path = 'reddit-data-100-posts.json'

with open(file_path) as file:
  data = json.load(file)

"""
stats I want to keep track of

- average words per post
"""
num_posts = len(data)

def get_stats():
    longest_post = 0
    shortest_post = 10000000
    total_words = 0
    for post in data:
        len_post = len(post['title'].split(' ')) + len(post['selftext'].split(' '))
        total_words += len_post
        longest_post = max(len_post, longest_post)
        shortest_post = min(len_post, shortest_post)
    return  total_words / num_posts, longest_post, shortest_post

len_post_hist = []
for post in data:
    len_post_hist.append(len(post['title'].split(' ')) + len(post['selftext'].split(' ')))
print(statistics.median(len_post_hist))

temp = plt.hist(len_post_hist, bins=100, range=(2,100))
plt.xlabel("Number of Words Per Post")
plt.ylabel("Count")
plt.show()

score_post_hist = []
for post in data:
    score_post_hist.append(post['score'])
print("Mean", statistics.mean(score_post_hist), "Median", statistics.median(score_post_hist))
print("Min", min(score_post_hist), "Max", max(score_post_hist))

temp = plt.hist(score_post_hist, bins=40, range=(166,281741))
plt.xlabel("Score")
plt.ylabel("Count")
plt.show()

print(get_stats())

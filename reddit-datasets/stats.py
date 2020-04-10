import json
import numpy as np

with open('reddit-data-100-posts.json') as file:
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
        if len_post == 2:
            print(post)
    return  total_words / num_posts, longest_post, shortest_post

print(get_stats())

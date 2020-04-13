import json
import re
import pickle

file_path_name = 'reddit-datasets/reddit-data-1-post'
file_path = file_path_name + ".json"
"""
this file is to filter out the array of posts based on the following filters:

- posts with fewer than 3 words in the title and body combined
"""


# LOAD DATA
with open(file_path) as file:
    data = json.load(file)

# FILTERS


def is_too_short(post):
    return len(post['title'].split(' ')) + len(post['selftext'].split(' ')) < 3


filters = [is_too_short]

# given a post, determine whether or not we should filter it


def should_filter(post):
    for my_filter in filters:
        if my_filter(post):
            print("...filtering " + post['subreddit'])
            return False
    return True


# RUN ALL FILTERS
processed_data = list(filter(should_filter, data))

# ADD TOKENS TO EACH POST


def tokenize(text):
    lowercase_text = text.lower()
    return re.findall(r'[a-z]+', lowercase_text)


def tokenize_post(post, tokenizer=tokenize):
    words_title = tokenizer(post['title'].lower())
    words_body = tokenizer(post['selftext'].lower())
    words_title.extend(words_body)
    return words_title


count = 0

for post in processed_data:
    post['id'] = count
    post['tokens'] = tokenize_post(post)
    count += 1

# create json with updated tokens
with open(file_path_name + "-processed.json", 'w') as outfile:
    json.dump(processed_data, outfile)

# create pickle with updated tokens
pickle.dump(processed_data, open(file_path_name + "-processed.pickle", 'wb'))

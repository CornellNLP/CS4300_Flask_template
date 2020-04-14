import json
import re
import pickle
from shared_variables import file_path
from shared_variables import file_path_name
from shared_variables import original_dataset_path
from create_structures import load_data

"""
this file is to filter out the array of posts based on the following filters:

- posts with fewer than 3 words in the title and body combined
"""

def load_data():
    #open original, unfiltered dataset
    with open(original_dataset_path) as file:
        return json.load(file)

# FILTERS
def is_too_short(post):
    return len(post['title'].split(' ')) + len(post['selftext'].split(' ')) < 3

# given a post, determine whether or not we should filter it

def should_filter(post):
    filters = [is_too_short]
    for my_filter in filters:
        if my_filter(post):
            print("...filtering " + post['subreddit'])
            return False
    return True


def tokenize(text):
    lowercase_text = text.lower()
    return re.findall(r'[a-z]+', lowercase_text)


def tokenize_post(post, tokenizer=tokenize):
    words_title = tokenizer(post['title'].lower())
    words_body = tokenizer(post['selftext'].lower())
    words_title.extend(words_body)
    return words_title


def process_data():
    data = load_data()
    processed_data = list(filter(should_filter, data))

    count = 0

    for post in processed_data:
        post['id'] = count
        post['tokens'] = tokenize_post(post)
        count += 1

    # create json with updated tokens
    with open(file_path, 'w') as outfile:
        json.dump(processed_data, outfile)

    # create pickle with updated tokens
    pickle.dump(processed_data, open(file_path_name + '.pickle', 'wb'))

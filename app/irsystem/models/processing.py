import json
import re
import pickle
from app.irsystem.models.shared_variables import file_path
from app.irsystem.models.shared_variables import file_path_name
from app.irsystem.models.shared_variables import num_posts
from app.irsystem.models.shared_variables import min_words_per_post
from app.irsystem.models.create_structures import load_data
from collections import Counter

"""
this file is to filter out the array of posts based on the following filters:

- posts with fewer than 3 words in the title and body combined
"""

fields_we_care_about = ['author', 'created_utc', 'score', 'selftext', 'subreddit', 'total_awards_received', 'title', 'subreddit_subscribers']
default = ['', 0 , 0, '', 'danger-no-subreddit', 0, '', 0]

def load_data():
    with open(file_path) as file:
        return json.load(file)

# FILTERS
def is_too_short(post):
    return 'selftext' in post and 'title' in post and len(post['title'].split(' ')) + len(post['selftext'].split(' ')) < min_words_per_post

#figure out if post contains an image, we should ignore those
def is_img_post(post):
    return False

def is_not_appropriate(post):
    return 'over_18' in post and post['over_18']

# given a post, determine whether or not we should filter it

def should_keep(post):
    filters = [is_too_short, is_img_post, is_not_appropriate]
    filterNames = ["too short", "is image post", "is not appropriate"]
    for i in range(len(filters)):
        my_filter = filters[i]
        name = filterNames[i]
        if my_filter(post):
            return False, name
    return True, ""


def tokenize(text):
    return re.findall(r'[a-z]+', text.lower())


def tokenize_post(post, tokenizer=tokenize):
    words_title = tokenizer(post['title'].lower())
    words_body = tokenizer(post['selftext'].lower())
    words_title.extend(words_body)
    return words_title

def process_post(post):
    is_valid_post, message = should_keep(post)
    if(is_valid_post):
        shortened_post = {}
        for field in fields_we_care_about:
            if not field in post:
                shortened_post[field] = default[fields_we_care_about.index(field)]
            else:
                shortened_post[field] = post[field]
        shortened_post['tokens'] = tokenize_post(shortened_post)

        #remove the title and body of the post to lessen the size of the dataset
        del shortened_post['selftext']
        del shortened_post['title']

        return True, shortened_post, None
    return False, None, message

def remove_low_subreddit_counts(dataset):
    count = Counter()

    for post in dataset:
        count[post['subreddit']] += 1

    invalid_subreddits = set()
    for subreddit, freq in count.most_common():
        if freq < num_posts * 0.1 : #don't include subreddits with fewer than 10% of original queried posts
            invalid_subreddits.add(subreddit.lower())

    finalized_dataset = []
    index = 0
    for post in dataset:
        if not post['subreddit'].lower() in invalid_subreddits:
            post['id'] = index
            index += 1
            finalized_dataset.append(post)
        else:
            print("removing: " + post['subreddit'])
    return finalized_dataset


"""
creates a new json with an additional "-manually-added" part of the name added
to avoid overwriting an exisiting json

in order to be used, the "-manually-added" must be removed from the name of the file,
which may overwrite an exisiting file. Here is where you must check that process_data()
actually performed as planned.
"""
def process_data():
    data = load_data()
    filtered_data = list(filter(should_keep, data))
    final_dataset = remove_low_subreddit_counts(data)
    # create json with updated tokens
    with open(file_path_name + '-manually-added.json', 'w') as outfile:
        json.dump(final_dataset, outfile)

    # # create pickle with updated tokens
    # pickle.dump(processed_data, open(file_path_name + '.pickle', 'wb'))

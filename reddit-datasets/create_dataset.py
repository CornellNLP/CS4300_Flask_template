import requests
import csv
import json
import time
from shared_variables import num_posts
from shared_variables import original_dataset_path
"""
script is used to create a json of the top n posts for the top 100 subreddits
"""
fields_we_care_about = ['author', 'created_utc', 'score', 'selftext', 'subreddit', 'total_awards_received', 'title', 'subreddit_subscribers']
default = ['', 0 , 0, '', 'danger-no-subreddit', 0, '', 0]
time_between_calls = 0.5 #seconds

def make_query(subreddit):
    query_prefix="https://api.pushshift.io/reddit/search/submission/?subreddit="
    query_suffix="&sort=desc&sort_type=score&size="
    str_num_posts=str(num_posts)
    return query_prefix + subreddit + query_suffix + str_num_posts

def create_dataset():
    dataset = []
    with open("reddit-datasets/top100.csv") as csvfile:
        reader = csv.reader(csvfile)
        for subreddit in reader:
            print("query:" + str(make_query(subreddit[0])), "\n")

            #set time between calls so as to not get a throttling error
            time.sleep(time_between_calls)

            raw_response = requests.get(make_query(subreddit[0]))
            response = raw_response.json()
            data = response['data']

            for post in data:
                if post['over_18']:
                    print("ignoring " + subreddit[0])
                    continue
                shortend_post = {}
                for field in fields_we_care_about:
                    if not field in post:
                        shortend_post[field] = default[fields_we_care_about.index(field)]
                    else:
                        shortend_post[field] = post[field]
                dataset.append(shortend_post)

    with open(original_dataset_path, 'w') as outfile:
        json.dump(dataset, outfile)

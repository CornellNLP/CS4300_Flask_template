import requests
import csv
import json


"""
script is used to create a json of the top 100 posts for the top 100 subreddits
"""

fields_we_care_about = ['author', 'created_utc', 'score', 'selftext', 'subreddit', 'total_awards_received', 'title', 'subreddit_subscribers']
default = ['', 0 , 0, '', 'danger-no-subreddit', 0, '', 0]
def make_query(subreddit):
    query_prefix="https://api.pushshift.io/reddit/search/submission/?subreddit="
    query_suffix="&sort=desc&sort_type=score&size="
    num_posts=str(100)
    return query_prefix + subreddit + query_suffix + num_posts

dataset = []
with open("top100.csv") as csvfile:
    reader = csv.reader(csvfile)
    for subreddit in reader:
        print("querying: " + subreddit[0])
        print("query:" + str(make_query(subreddit[0])), "\n")
        response = requests.get(make_query(subreddit[0])).json()
        data = response['data']
        for post in data:
            shortend_post = {}
            for field in fields_we_care_about:
                if not field in post:
                    shortend_post[field] = default[fields_we_care_about.index(field)]
                else:
                    shortend_post[field] = post[field]
            dataset.append(shortend_post)

with open('top-100-reddit-data.txt', 'w') as outfile:
    json.dump(dataset, outfile)

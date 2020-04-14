import requests
import csv
import json
import time
from collections import Counter
from shared_variables import num_posts
from shared_variables import file_path
from shared_variables import reddit_list
from processing import process_post

"""
script is used to create a json of the top n posts for the top 100 subreddits
"""

time_between_calls = 0.2 #seconds

def make_query(subreddit):
    query_prefix="https://api.pushshift.io/reddit/search/submission/?subreddit="
    query_suffix="&sort=desc&sort_type=score&size="
    str_num_posts=str(num_posts)
    return query_prefix + subreddit + query_suffix + str_num_posts

def create_dataset():
    dataset = []
    with open(reddit_list) as csvfile:
        reader = csv.reader(csvfile)

        #keep track of number of posts in the subreddit
        cnt = Counter()

        #for ids
        count = 0
        for subreddit in reader:
            print("query: " + str(make_query(subreddit[0])), "\n")

            #set time between calls so as to not get a throttling error
            time.sleep(time_between_calls)

            raw_response = requests.get(make_query(subreddit[0]))
            response = raw_response.json()
            data = response['data']

            for post in data:
                success, ppost = process_post(post)
                if(success):
                    cnt[subreddit[0]] += 1
                    ppost['id'] = count
                    count += 1
                    dataset.append(ppost)
        invalid_subreddits = set()
        for subreddit_name, freq in cnt.most_common():
            if freq < num_posts * 0.1: #don't include subreddits with fewer than 10% of posts
                invalid_subreddits.add(subreddit_name)
                print("removing " + subreddit_name + " with a low count " + str(freq))
        finalized_dataset = []
        for post in dataset:
            if not post['subreddit'].lower() in invalid_subreddits:
                finalized_dataset.append(post)

    with open(file_path, 'w') as outfile:
        json.dump(finalized_dataset, outfile)

import requests
import csv
import json
import time
from collections import Counter
from app.irsystem.models.shared_variables import num_posts
from app.irsystem.models.shared_variables import file_path
from app.irsystem.models.shared_variables import reddit_list
from app.irsystem.models.shared_variables import num_subreddits
from app.irsystem.models.processing import process_post

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
    with open(reddit_list) as csvfile:
        reader = csv.reader(csvfile)

        #keep track of number of posts in the subreddit
        cnt = Counter()

        #keep track of initial, unprocessed data
        dataset = []

        #keep track of how many subreddits we have processed
        subreddit_counter = 0

        #do not query the same subreddit multiple times
        subreddit_query_history = set()

        for subreddit_row in reader:
            print("***********************************")
            subreddit = subreddit_row[0].lower()

            if(subreddit in subreddit_query_history):
                print("duplicate subreddit in list: " + subreddit)
                continue

            subreddit_counter += 1
            if(subreddit_counter > num_subreddits):
                break

            subreddit_query_history.add(subreddit)

            print(str(subreddit_counter) + " query: " + str(make_query(subreddit)), "\n")

            #set time between calls so as to not get a throttling error
            time.sleep(time_between_calls)

            #make query to api
            raw_response = requests.get(make_query(subreddit))
            response = raw_response.json()
            data = response['data']

            message_count = Counter()

            #if post passes all of our filters, add to dataset
            for post in data:
                success, ppost, message = process_post(post)

                if(success):
                    cnt[subreddit] += 1
                    dataset.append(ppost)
                else:
                    message_count[message] += 1

            #print information about how each post was
            for message, count in message_count.most_common():
                print("     " + str(count) + " " + str(message))

        #don't include subreddits with fewer than 10% of posts
        invalid_subreddits = set()
        for subreddit_name, freq in cnt.most_common():
            if freq < num_posts * 0.20:
                invalid_subreddits.add(subreddit_name)
                print("removing " + subreddit_name + " with a low count " + str(freq))

        finalized_dataset = []
        count = 0
        for post in dataset:
            if not post['subreddit'].lower() in invalid_subreddits:
                finalized_dataset.append(post)
                post['id'] = count
                count += 1


    with open(file_path, 'w') as outfile:
        json.dump(finalized_dataset, outfile)

"""
Script that gets the top NUM_JOKES in subreddit r/Jokes.
"""

import praw
import json

NUM_JOKES = 5000

#creates a praw API instance
reddit = praw.Reddit(client_id = '0oidSfIOuXzx1w',
                     client_secret = '2ZesBSgpQ0BS8FVFpePRJqLEwqM',
                     user_agent = 'joke getter')

subreddit = reddit.subreddit('jokes') # Subreddit Jokes
posts = subreddit.top(limit=NUM_JOKES) # Obtains top NUM_JOKES posts/submissions

jokes = [] # accumulated list of dictionaries, with entries 'joke', 'score', and 'categories'

try:
    for post in posts:
        new_joke = {}
        new_joke['joke'] = post.title + ' ' + post.selftext
        new_joke['score'] = post.score
        new_joke['categories'] = []
        # for debugging purposes
        # print("Joke: {}, Score: {}".format(new_joke['joke'], new_joke['score']))
        jokes.append(new_joke)
finally:
    with open('./json/raw/reddit_jokes_raw.json', 'w') as file:
        json.dump(jokes, file, indent=4)

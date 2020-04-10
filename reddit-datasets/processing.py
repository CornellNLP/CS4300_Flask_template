import json

file_path = 'reddit-data-100-posts.json'

with open(file_path) as file:
  data = json.load(file)
#FILTERS
def is_too_short(post):
    return len(post['title'].split(' ')) + len(post['selftext'].split(' ')) < 3

#TODO: add more filters here, and to the filter array underneath

filters = [is_too_short]

#given a post, determine whether or not we should filter it
def should_filter(post):
    for my_filter in filters:
        if my_filter(post):
            print("...filtering " + post['subreddit'])
            return False
    return True

processed_data = list(filter(should_filter, data))

with open('top-1000-reddit-data-processed.json', 'w') as outfile:
    json.dump(processed_data, outfile)

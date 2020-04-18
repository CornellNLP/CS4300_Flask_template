import os

this_dir = os.path.dirname(os.path.abspath(__file__))
jar = this_dir + "/picklejar/"
num_posts = 500
num_subreddits = 800
min_words_per_post = 20
num_partitions = 10 #for the inverted index
max_document_frequency = 0.1
"""
DATASET NAMING CONVENTION
""<num posts>p<num subreddits>s<min words per post>mwc.json"
Example: 1000p700s10mwc.json
"""
file_path_name = jar + str(num_posts) + 'p' + str(num_subreddits) + 's' + str(min_words_per_post) + 'mwc'
file_path = file_path_name + ".json"
reddit_list = jar + 'subreddits.csv'

jar = "reddit-datasets/picklejar/"
num_posts = 1000
num_subreddits = 10000
min_words_per_post = 10

"""
DATASET NAMING CONVENTION
""<num posts>p<num subreddits>s<min words per post>mwc.json"
Example: 1000p700s10mwc.json
"""
file_path_name = jar + str(num_posts) + 'p' + str(num_subreddits) + 's' + str(min_words_per_post) + 'mwc'
file_path = file_path_name + ".json"
reddit_list = 'reddit-datasets/subreddits.csv'

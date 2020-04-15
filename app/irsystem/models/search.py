import pickle
import json
from app.irsystem.models.shared_variables import num_posts
from app.irsystem.models.shared_variables import jar
from app.irsystem.models.shared_variables import file_path
from app.irsystem.models.comparison import compare_string_to_posts
from app.irsystem.models.comparison import find_subreddits

#create the dataset from the pushshift api
#create_dataset()

#process the raw data taken from the api
#process_data()

#create the idf, inverted index, and norms
#create_and_store_structures()


def open_datastructures():
    with open(jar + str(num_posts) + "-inverted_index.pickle", 'rb') as file:
        inverted_index = pickle.load(file)

    with open(jar + str(num_posts) + "-idf.pickle", 'rb') as file:
        idf = pickle.load(file)

    with open(jar + str(num_posts) + "-norms.pickle", 'rb') as file:
        norms = pickle.load(file)

    with open(file_path) as file:
        post_list = json.load(file)

    return inverted_index, idf, norms, post_list

def full_search(query):
    inverted_index, idf, norms, post_list = open_datastructures()
    ranks = compare_string_to_posts(query, inverted_index, idf, norms)
    return find_subreddits(10, ranks, post_list)

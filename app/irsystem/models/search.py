import pickle
import json
import time
from app.irsystem.models.create_dataset import create_dataset
from app.irsystem.models.processing import process_data
from app.irsystem.models.create_structures import create_and_store_structures
from app.irsystem.models.shared_variables import file_path
from app.irsystem.models.shared_variables import file_path_name
from app.irsystem.models.comparison import compare_string_to_posts
from app.irsystem.models.comparison import find_subreddits

#create the dataset from the pushshift api
# print("Looking at " + file_path_name)
# print("create dataset? this will make queries to the api and can take a long time y/n")
# ans = input()
# if ans == 'y':
#     create_dataset()


#create the idf, inverted index, and norms

print("create and store structures? y/n")
ans = input()
if ans == 'y':
    create_and_store_structures()

print("delay end.")
input()

def open_datastructures():
    with open(file_path_name + "-inverted_index.pickle", 'rb') as file:
        print("...loading inverted index")
        inverted_index = pickle.load(file)
        print("finished loading inverted index.")

    with open(file_path_name + "-idf.pickle", 'rb') as file:
        print("...loading idf")
        idf = pickle.load(file)
        print("finished loading idf.")

    with open(file_path_name + "-norms.pickle", 'rb') as file:
        print("...loading norms")
        norms = pickle.load(file)
        print("finished loading norms")

    with open(file_path_name + "-post_lookup.pickle", 'rb') as file:
        print("...loading posts")
        post_lookup = pickle.load(file)
        print("finished loading posts")
    return inverted_index, idf, norms, post_lookup

def run_tests(inverted_index, idf, norms, post_lookup):
    while True:
        print("\nquery: ", "")
        ranks = compare_string_to_posts(input(), inverted_index, idf, norms)
        print(find_subreddits(10, ranks, post_lookup))

def full_search(query):
    ranks = compare_string_to_posts(query, inverted_index, idf, norms)
    return find_subreddits(10, ranks, post_lookup)

inverted_index, idf, norms, post_lookup = open_datastructures()

import pickle
import json
from create_dataset import create_dataset
from processing import process_data
from create_structures import create_and_store_structures
from shared_variables import file_path
from shared_variables import file_path_name
from comparison import compare_string_to_posts
from comparison import find_subreddits
import time

#create the dataset from the pushshift api
# print("Looking at " + file_path_name)
# print("create dataset? this will make queries to the api and can take a long time y/n")
# ans = input()
# if ans == 'y':
#     create_dataset()


#create the idf, inverted index, and norms

# print("create and store structures? y/n")
# ans = input()
# if ans == 'y':
#     create_and_store_structures()


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

start = time.time()
inverted_index, idf, norms, post_lookup = open_datastructures()
end = time.time()
print("time to load datastructures: " + str(end - start))
run_tests(inverted_index, idf, norms, post_lookup)

import pickle
import json
import time
from collections import Counter
from app.irsystem.models.create_dataset import create_dataset
from app.irsystem.models.processing import process_data
from app.irsystem.models.create_structures import create_and_store_structures
from app.irsystem.models.shared_variables import file_path
from app.irsystem.models.shared_variables import file_path_name
from app.irsystem.models.comparison import compare_string_to_posts
from app.irsystem.models.comparison import find_subreddits
from app.irsystem.models.inverted_index import InvertedIndex

class SearchEngine():
    def __init__(self, should_build_structures):
        if should_build_structures:
            self.create()
        inverted_index, idf, norms, post_lookup, subreddit_lookup = self.open_datastructures()
        self.inverted_index = inverted_index
        self.idf = idf
        self.norms = norms
        self.post_lookup = post_lookup
        self.subreddit_lookup = subreddit_lookup

    def open_datastructures(self):
        print("...loading inverted index")
        inverted_index = InvertedIndex()
        inverted_index.load()
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
            print("# of posts: " + str(len(post_lookup.keys())))
            print("finished loading posts")

        with open(file_path_name + "-subreddit_lookup.pickle", 'rb') as file:
            print("...loading posts")
            subreddit_lookup = pickle.load(file)
            print("finished loading posts")

        return inverted_index, idf, norms, post_lookup, subreddit_lookup

    def run_tests(self, inverted_index, idf, norms, post_lookup, subreddit_lookup):
        while True:
            print("\nquery: ", "")
            ranks = compare_string_to_posts(input(), self.inverted_index, self.idf, self.norms)
            print(find_subreddits(10, ranks, self.post_lookup, self.subreddit_lookup))

    def search(self, query):
        ranks = compare_string_to_posts(query, self.inverted_index, self.idf, self.norms)
        return find_subreddits(10, ranks, self.post_lookup, self.subreddit_lookup)

    def create(self):
        #create the dataset from the pushshift api
        print("Looking at " + file_path_name)
        print("create dataset? this will make queries to the api and can take a long time y/n")
        ans = input()
        if ans == 'y':
            create_dataset()

        #create the idf, inverted index, and norms

        print("create and store structures? y/n")
        ans = input()
        if ans == 'y':
            create_and_store_structures()

        print("delay end.")
        input()

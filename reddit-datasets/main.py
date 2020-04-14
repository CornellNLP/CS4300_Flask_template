import pickle
import json
from create_dataset import create_dataset
from processing import process_data
from create_structures import create_and_store_structures
from shared_variables import num_posts
from shared_variables import jar
from shared_variables import file_path
from comparison import compare_string_to_posts
from comparison import find_subreddits
import time

#create the dataset from the pushshift api
#create_dataset()

#create the idf, inverted index, and norms
#create_and_store_structures()


def open_datastructures():
    with open(jar + str(num_posts) + "-inverted_index.pickle", 'rb') as file:
        print("...loading inverted index")
        inverted_index = pickle.load(file)
        print("finished loading inverted index.")

    with open(jar + str(num_posts) + "-idf.pickle", 'rb') as file:
        print("...loading idf")
        idf = pickle.load(file)
        print("finished loading idf.")

    with open(jar + str(num_posts) + "-norms.pickle", 'rb') as file:
        print("...loading norms")
        norms = pickle.load(file)
        print("finished loading norms")

    with open(file_path) as file:
        print("...loading posts")
        post_list = json.load(file)
        print("finished loading posts")
    return inverted_index, idf, norms, post_list

def run_tests(inverted_index, idf, norms, post_list):
    # test_query = "my cab driver tonight was so excited to share with me that he'd made the cover of the calendar i told him i'd help let the world see"
    # query1 = "I found out that a coworker in the same position"
    # query2 = "a mandatory class in high school that teaches about budgeting, handling or avoiding debt"
    # query3 = "He went for a full body soak instead"
    # query4 = "I think that the moon should be smaller than the sun because science"
    # query5 = "Hey dad, I'm hungry. Hi hungry I'm dad!"
    while True:
        print("\nquery: ", "")
        ranks = compare_string_to_posts(input(), inverted_index, idf, norms)
        print(find_subreddits(10, ranks, post_list))

start = time.time()
inverted_index, idf, norms, post_list = open_datastructures()
end = time.time()
print(end - start)
run_tests(inverted_index, idf, norms, post_list)

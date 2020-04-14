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

def run_tests(inverted_index, idf, norms, post_list):
    test_query = "my cab driver tonight was so excited to share with me that he'd made the cover of the calendar i told him i'd help let the world see"
    query1 = "I found out that a coworker in the same position"
    query2 = "a mandatory class in high school that teaches about budgeting, handling or avoiding debt"
    query3 = "He went for a full body soak instead"
    query4 = "I think that the moon should be smaller than the sun because science"
    query5 = "Hey dad, I'm hungry. Hi hungry I'm dad!"
    ranks = compare_string_to_posts(query5, inverted_index, idf, norms)
    print(find_subreddits(10, ranks, post_list))

inverted_index, idf, norms, post_list = open_datastructures()
run_tests(inverted_index, idf, norms, post_list)

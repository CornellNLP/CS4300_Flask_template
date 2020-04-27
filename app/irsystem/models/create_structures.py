from collections import defaultdict
from collections import Counter
import json
import math
import string
import pickle
import time
import numpy as np
from app.irsystem.models.shared_variables import file_path
from app.irsystem.models.shared_variables import file_path_name
from app.irsystem.models.shared_variables import max_document_frequency
from app.irsystem.models.inverted_index import InvertedIndex
"""
this file is to create datastructures. Currently creates:

- inverted index
"""


def load_data():
    # open the already filtered dataset
    with open(file_path) as file:
        return json.load(file)


"""
  Makes an inverted index from given file (list of posts)
  Returns: inverted index as a dictionary
  list of tuples of (post_id, term_count)
"""


def make_inverted_index(data):
    i = InvertedIndex()
    i.create(data)
    return i


"""
Compute IDF values from the inverted index
Returns: idf dictionary {term: idf value}
"""


def get_idf(inv_index, num_docs, min_df=0, max_df=0.1):  # TODO: change these min/max in the future
    idf = {}
    max_rat = max_df * num_docs
    for k, v in inv_index.items():
        df = len(v)
        if df >= min_df and df <= max_rat:
            idf[k] = num_docs / float(df)
    return idf


"""
  Computes norm of each document
  Returns: dict where {doc_id: norm of doc}
"""


def get_doc_norms(inv_index, idf, num_docs):
    norms = {}

    for k, v in inv_index.items():
        idf_i = idf[k]
        for pair in v:
            i = pair[0]
            tf = pair[1]
            if i not in norms:
                norms[i] = (tf*idf_i)**2
            else:
                norms[i] += (tf*idf_i)**2

    for k, v in norms.items():
        norms[k] = v**(0.5)

    return norms

def make_post_subreddit_lookup(data, inverted_index):
    post_lookup = {}
    subreddit_lookup = {}
    for post in data:
        post_lookup[post['id']] = {}
        post_lookup[post['id']]['subreddit'] = post['subreddit']
        cnt = Counter()
        for token in post['tokens']:
            if token in inverted_index:
                cnt[token] += 1
        post_lookup[post['id']]['word_count'] = cnt.most_common()
        if not post['subreddit'] in subreddit_lookup:
            subreddit_lookup[post['subreddit']] = 0
        subreddit_lookup[post['subreddit']] += 1
    return post_lookup, subreddit_lookup

def create_and_store_structures():
    print("...creating structures")

    print("...loading data")
    data = load_data()
    num_docs = len(data)

    print("...making inverted index(will take a long time)")
    inverted_index = make_inverted_index(data)

    print("...computing idf")
    idf = get_idf(inverted_index, num_docs, 0, max_document_frequency)

    print("...pruning inverted index")
    #remove values that were removed from the idf
    tokens = inverted_index.keys()
    for token in tokens:
        if not token in idf:
            inverted_index.remove_token(token)

    print("...making subreddit lookup")
    post_lookup, subreddit_lookup = make_post_subreddit_lookup(data, inverted_index)

    print("...getting doc norms")
    norms = get_doc_norms(inverted_index, idf, num_docs)

    # store data in pickle files

    print("...storing post lookup")
    pickle.dump(post_lookup, open(file_path_name + "-post_lookup.pickle", 'wb'))
    print("...storing subreddit lookup")
    pickle.dump(subreddit_lookup, open(file_path_name + "-subreddit_lookup.pickle", 'wb'))
    print("...storing inverted index")
    inverted_index.store()
    print("...storing idf")
    pickle.dump(idf, open(file_path_name + "-idf.pickle", 'wb'))
    print("...storing doc norms")
    pickle.dump(norms, open(file_path_name + "-norms.pickle", 'wb'))
    print("completed creating and storing structures.")

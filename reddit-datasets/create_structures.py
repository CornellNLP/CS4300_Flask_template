from collections import defaultdict
from collections import Counter
import json
import math
import string
import time
import numpy as np
# from nltk.tokenize import TreebankWordTokenizer
# from IPython.core.display import HTML
file_path_name = 'reddit-datasets/reddit-data-1-post-processed'
file_path = file_path_name + ".json"

"""
this file is to create datastructures. Currently creates:

- inverted index
"""

# LOAD DATA
with open(file_path) as file:
    data = json.load(file)

num_docs = len(data)

"""
  Makes an inverted index from given file
  Returns: inverted index as a dictionary
  list of tuples of (post_id, term_count)
"""


def make_inverted_index(file):
    inv_index = {}

    for i in range(0, len(file)):
        temp_dict = {}
        words = file[i]['tokens']
        for w in words:
            if w not in temp_dict:
                temp_dict[w] = 1
            else:
                temp_dict[w] += 1
        for k, v in temp_dict.items():
            if k not in inv_index:
                inv_index[k] = []
            inv_index[k].append((i, temp_dict[k]))
    return inv_index


inverted_index = make_inverted_index(data)

"""
Compute IDF values from the inverted index
Returns: idf dictionary {term: idf value}
"""


def get_idf(inv_index, num_docs, min_df=0, max_df=1):  # TODO: change these min/max in the future
    idf = {}
    max_rat = max_df * num_docs

    for k, v in inv_index.items():
        df = len(v)
        if df >= min_df and df <= max_rat:
            idf[k] = 1 / float(df)
    return idf


idf = get_idf(inverted_index, num_docs)

"""
  Computes norm of each document
  Returns: np.array where norms[i] = norm of document i
"""


def get_doc_norms(inv_index, idf, num_docs):
    norms = np.zeros(num_docs)

    for k, v in inv_index.items():
        if k in idf:
            idf_i = idf[k]
            for pair in v:
                i = pair[0]
                tf = pair[1]
                norms[i] += (tf*idf_i)**2

    norms = np.sqrt(norms)

    return norms


norms = get_doc_norms(inverted_index, idf, num_docs)

"""
    Computes cosine similarity between the given query and all the posts
    Assumse query is given as tokenized already
    Returns: dictionary of cosine similarities where {index: cossim}
"""


def get_cossim(query, inv_index, idf, norms):
    query_tf = {}  # term frequency of query
    for token in query:
        wordcount = query.count(token)
        if token not in query_tf:
            query_tf[token] = wordcount
    dot_prod = {}
    for token in query:
        if token in inv_index:
            posts = inv_index[token]
        # if token in idf:              do we need this if statement
            for index, tf in posts:
                if index not in dot_prod:
                    dot_prod[index] = 0
                dot_prod[index] += (tf*idf[token]) * (query_tf[token]*idf[token])
    query_norm = 0
    for tf in query_tf:
        if tf in idf:
            query_norm += (query_tf[tf] * idf[tf])**2
    query_norm = query_norm**(0.5)
    cos_sim = {}
    for k, v in dot_prod.items():
        cos_sim[k] = dot_prod[k] / (query_norm * norms[k])
    return cos_sim


test_query = [
    "my",
    "cab",
    "driver",
    "tonight",
    "was",
    "so",
    "excited",
    "to",
    "share",
    "with",
    "me",
    "that",
    "he",
    "d",
    "made",
    "the",
    "cover",
    "of",
    "the",
    "calendar",
    "i",
    "told",
    "him",
    "i",
    "d",
    "help",
    "let",
    "the",
    "world",
    "see"
]


# TODO: this print statement is returning 1.23825871347 when cossim should never return
# more than 1. It should be returning 1 since our test query is the same as the post 1.
print(get_cossim(test_query, inverted_index, idf, norms)[1])

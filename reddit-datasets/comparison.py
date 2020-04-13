import pickle
import json
import re
from collections import Counter 
from create_structures import file_path
from processing import tokenize
"""
    Unpickle our data structures
"""

jar = "reddit-datasets/picklejar/"

pkl1 = open(jar + "inverted_index.pickle", 'rb')
pkl2 = open(jar + "idf.pickle", 'rb')
pkl3 = open(jar + "norms.pickle", 'rb')

inverted_index = pickle.load(pkl1)
idf = pickle.load(pkl2)
norms = pickle.load(pkl3)

pkl1.close()
pkl2.close()
pkl3.close()

"""
    Grabbing data from the JSON
"""

with open(file_path) as file:
    post_list = json.load(file)

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
    for token in set(query):
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

"""
    Returns the post ids of the top x posts that match the query
    TODO: make more complicated (ML, etc.) later
"""
def comparison(top_x, query):
    top_dict = get_cossim(query, inverted_index, idf, norms)
    k = Counter(top_dict)
    return [x[0] for x in k.most_common(top_x)]


"""
    Top-level function, outputs list of subreddits for each post in
    post_ids (set of unique subreddit names)
"""
def find_subreddits(post_ids):
    return set([post_list[i]['subreddit'] for i in post_ids])

test_query = "my cab driver tonight was so excited to share with me that he'd made the cover of the calendar i told him i'd help let the world see"
query1 = "I found out that a coworker in the same position"
query2 = "a mandatory class in high school that teaches about budgeting, handling or avoiding debt"
query3 = "He went for a full body soak instead"

# TODO: this print statement is returning 1.23825871347 when cossim should never return
# more than 1. It should be returning 1 since our test query is the same as the post 1.
 

print(find_subreddits(comparison(10, tokenize(query3))))

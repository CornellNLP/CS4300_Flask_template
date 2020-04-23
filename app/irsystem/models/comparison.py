import pickle
import json
import re
import math
from collections import Counter
from app.irsystem.models.shared_variables import file_path
from app.irsystem.models.shared_variables import jar
from app.irsystem.models.shared_variables import max_document_frequency
from app.irsystem.models.processing import tokenize
from app.irsystem.models.inverted_index import InvertedIndex

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
        if token in inv_index and token in idf:
            posts = inv_index[token]
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
def comparison(query, inverted_index, idf, norms):
    top_dict = get_cossim(query, inverted_index, idf, norms)
    return Counter(top_dict).most_common()

def compare_string_to_posts(query, inverted_index, idf, norms):
    return comparison(inverted_index.getStem(tokenize(query)), inverted_index, idf, norms)

"""
    Top-level function, outputs list of subreddits for each post in
    post_ids (set of unique subreddit names)
"""
def find_subreddits(top_x, post_ids, post_lookup, subreddit_lookup):
    #need to group posts by subreddit
    subreddit_dict = {}
    subreddit_freq = {}

    for post_id, score in post_ids:
        #need to get the post associated with this post id
        subreddit = post_lookup[post_id]
        if subreddit not in subreddit_dict:
            subreddit_dict[subreddit] = 0
            subreddit_freq[subreddit] = 0
        subreddit_dict[subreddit] += score
        subreddit_freq[subreddit] += 1

    k = Counter(subreddit_dict)

    for x in k.most_common(top_x):
        print(x[0] + "    "  + str(subreddit_freq[x[0]]) + "   " + str(subreddit_lookup[x[0]]) + "   " + str(x[1]))

    normalized = [(x[0], float(x[1]) * float(subreddit_freq[x[0]]) / float(subreddit_lookup[x[0]])) for x in k.most_common(top_x)]
    print(normalized)
    return sorted(normalized, key=lambda x: x[1], reverse=True)

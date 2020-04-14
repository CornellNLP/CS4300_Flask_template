import pickle
import json
import re
from collections import Counter
from shared_variables import file_path
from shared_variables import jar
from processing import tokenize

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
def comparison(query, inverted_index, idf, norms):
    top_dict = get_cossim(query, inverted_index, idf, norms)
    return Counter(top_dict).most_common()

def compare_string_to_posts(query, inverted_index, idf, norms):
    return comparison(tokenize(query), inverted_index, idf, norms)

"""
    Top-level function, outputs list of subreddits for each post in
    post_ids (set of unique subreddit names)
"""
def find_subreddits(top_x, post_ids, post_list):
    #need to group posts by subreddit
    subreddit_dict = {}
    subreddit_freq = {}
    for post, score in post_ids:
        subreddit = post_list[post]['subreddit']
        if subreddit not in subreddit_dict:
            subreddit_dict[subreddit] = 0
            subreddit_freq[subreddit] = 0
        subreddit_dict[subreddit] += score
        subreddit_freq[subreddit] += 1
    #TODO: normalize based on # of posts in the subreddit

    k = Counter(subreddit_dict)
    normalized = [(x[0], x[1] / float(subreddit_freq[x[0]])) for x in k.most_common(top_x)]
    return sorted(normalized, key=lambda x: x[1], reverse=True)

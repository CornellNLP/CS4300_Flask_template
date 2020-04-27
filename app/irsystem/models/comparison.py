import pickle
import json
import re
import math
from collections import Counter
from app.irsystem.models.shared_variables import file_path
from app.irsystem.models.shared_variables import jar
from app.irsystem.models.shared_variables import max_document_frequency
from app.irsystem.models.shared_variables import pseudo_relevance_rocchio_top_posts
from app.irsystem.models.shared_variables import pseudo_relevance_rocchio_lowest_posts
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
    top_dict = get_cossim(inverted_index.get_stem_of_words(query), inverted_index, idf, norms)
    return Counter(top_dict).most_common()

def compare_string_to_posts(query, inverted_index, idf, norms, post_lookup):
    tokenized_query = tokenize(query)
    stemmed_query = inverted_index.get_stem_of_words(tokenized_query)
    scores = comparison(tokenize(query), inverted_index, idf, norms)
    if(len(scores) < 0):
        return scores

    new_query = rocchio(stemmed_query, scores, post_lookup)

    print(new_query)

    updated_scores = comparison(new_query, inverted_index, idf, norms)
    return updated_scores

def sort_similarity_scores(sim_scores):
    return sorted(sim_scores, key=lambda x: x[1], reverse=True)

def sum_posts(sim_scores, post_lookup):
    count = Counter()
    for post_id, score in sim_scores:
        tokens = post_lookup[post_id]['word_count']
        for token, freq in tokens:
            count[token] += freq
    return count.most_common()

def sum_queries(q0, q1):
    count = Counter()
    for word, freq in q0:
        count[word] += freq
    for word, freq in q1:
        count[word] += freq
    count += Counter()
    return count.most_common()

def mult_posts(word_freq, const):
    return [(word, const * freq) for word, freq in word_freq]

"""
Given the results of the original query, update the query using the top
10 posts as the most accurate ones
"""
def rocchio(original_tokenized_query, sim_scores, post_lookup):
    a = 1 # how much we weigh the orignal query
    b = 1 # how much we weigh the similar posts
    c = 0
    #create list of word:freq
    query_count = Counter(original_tokenized_query)

    q0 = mult_posts(query_count.most_common(), a)
    #assume top n are relevant
    sorted_sim = sort_similarity_scores(sim_scores)

    #for each relevant doc, sum up freq of each word
    rel_count = sum_posts(sorted_sim[:pseudo_relevance_rocchio_top_posts], post_lookup)
    rel_count = mult_posts(rel_count, float(b / pseudo_relevance_rocchio_top_posts))

    #for each irrelevant doc, sum up freq of each word
    # num_irrel = min(pseudo_relevance_rocchio_lowest_posts, len(sorted_sim) - pseudo_relevance_rocchio_top_posts)
    # irrel_count = []
    # if(num_irrel > 0):
    #     irrel_count = sum_posts(sorted_sim[-pseudo_relevance_rocchio_lowest_posts:], post_lookup)
    #     irrel_count = mult_posts(irrel_count, -1 * float(c / num_irrel))
    #     q0 = sum_queries(q0, irrel_count)
    q1 = sum_queries(q0, rel_count)[:math.ceil(len(original_tokenized_query) * 1.2)]
    #double the length of the initial query
    new_query = []

    for word, score in q1:
        num_word = math.ceil(score)
        for i in range(num_word):
            new_query.append(word)
    return new_query
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
        subreddit = post_lookup[post_id]['subreddit']
        if subreddit not in subreddit_dict:
            subreddit_dict[subreddit] = 0
            subreddit_freq[subreddit] = 0
        subreddit_dict[subreddit] += score
        subreddit_freq[subreddit] += 1

    k = Counter(subreddit_dict)

    # for x in k.most_common(top_x):
    #     print(x[0] + "    "  + str(subreddit_freq[x[0]]) + "   " + str(subreddit_lookup[x[0]]) + "   " + str(x[1]))

    normalized = [(x[0], float(x[1]) * float(subreddit_freq[x[0]]) / float(subreddit_lookup[x[0]])) for x in k.most_common()]
    # print(normalized[:10])
    return sort_similarity_scores(normalized)[:10]
